import React, { useState, useEffect } from 'react'
import GameBoard from './components/GameBoard'
import PromoCodeModal from './components/PromoCodeModal'
import GameOverModal from './components/GameOverModal'
import ErrorMessage from './components/ErrorMessage'
import './App.css'

function App() {
  const [gameId, setGameId] = useState(null)
  const [board, setBoard] = useState(Array(5).fill('').map(() => Array(5).fill('')))
  const [gameStatus, setGameStatus] = useState('playing')
  const [winner, setWinner] = useState(null)
  const [promocode, setPromocode] = useState(null)
  const [showPromoModal, setShowPromoModal] = useState(false)
  const [showGameOverModal, setShowGameOverModal] = useState(false)
  const [gameMessage, setGameMessage] = useState('')
  const [chatId, setChatId] = useState(localStorage.getItem('chatId') || '')
  const [error, setError] = useState(null)
  const [loading, setLoading] = useState(false)

  const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api'

  const startNewGame = async () => {
    setLoading(true)
    setError(null)

    let timeoutId = null

    try {
      // Используем AbortController для совместимости со старыми браузерами
      const controller = new AbortController()
      timeoutId = setTimeout(() => controller.abort(), 10000)

      const response = await fetch(`${API_BASE_URL}/game/start`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        signal: controller.signal
      })

      if (timeoutId) clearTimeout(timeoutId)

      if (!response.ok) {
        const errorData = await response.json().catch(() => ({}))
        throw new Error(errorData.detail || `Ошибка сервера: ${response.status}`)
      }

      const data = await response.json()

      if (!data.game_id || !data.board) {
        throw new Error('Неверный формат ответа от сервера')
      }

      setGameId(data.game_id)
      setBoard(data.board)
      setGameStatus(data.status)
      setWinner(null)
      setPromocode(null)
      setShowPromoModal(false)
      setShowGameOverModal(false)
      setGameMessage('')
    } catch (error) {
      // Очищаем таймаут в случае ошибки
      if (timeoutId) clearTimeout(timeoutId)
      console.error('Ошибка при запуске игры:', error)

      let errorMessage = 'Не удалось начать игру. '

      if (error.name === 'TimeoutError' || error.name === 'AbortError') {
        errorMessage += 'Превышено время ожидания. Проверьте подключение к интернету.'
      } else if (error.message.includes('Failed to fetch') || error.message.includes('NetworkError')) {
        errorMessage += 'Не удалось подключиться к серверу. Убедитесь, что Backend запущен на http://localhost:8000'
      } else {
        errorMessage += error.message || 'Произошла неизвестная ошибка'
      }

      setError(errorMessage)

      // Автоматически скрыть ошибку через 5 секунд
      setTimeout(() => setError(null), 5000)
    } finally {
      setLoading(false)
    }
  }

  const makeMove = async (row, col) => {
    if (gameStatus !== 'playing' || board[row][col] !== '' || loading) {
      return
    }

    setLoading(true)
    setError(null)

    let timeoutId = null

    try {
      // Валидация перед отправкой
      if (!gameId) {
        throw new Error('Игра не инициализирована. Попробуйте начать новую игру.')
      }

      if (row < 0 || row >= 5 || col < 0 || col >= 5) {
        throw new Error('Неверные координаты хода')
      }

      // Используем AbortController для совместимости со старыми браузерами
      const controller = new AbortController()
      timeoutId = setTimeout(() => controller.abort(), 10000)

      const response = await fetch(`${API_BASE_URL}/game/move`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          game_id: gameId,
          row,
          col,
          chat_id: chatId || undefined
        }),
        signal: controller.signal
      })

      if (timeoutId) clearTimeout(timeoutId)

      if (!response.ok) {
        const errorData = await response.json().catch(() => ({}))
        throw new Error(errorData.detail || `Ошибка сервера: ${response.status}`)
      }

      const data = await response.json()

      // Валидация ответа
      if (!data.board || !Array.isArray(data.board)) {
        throw new Error('Неверный формат ответа от сервера')
      }

      setBoard(data.board)
      setGameStatus(data.status)

      if (data.status === 'finished') {
        setWinner(data.winner)
        setGameMessage(data.message)

        if (data.winner === 'player' && data.promocode) {
          setPromocode(data.promocode)
          setShowPromoModal(true)
        } else {
          setShowGameOverModal(true)
        }
      }
    } catch (error) {
      // Очищаем таймаут в случае ошибки
      if (timeoutId) clearTimeout(timeoutId)
      console.error('Ошибка при ходе:', error)

      let errorMessage = 'Не удалось выполнить ход. '

      if (error.name === 'TimeoutError' || error.name === 'AbortError') {
        errorMessage += 'Превышено время ожидания. Проверьте подключение.'
      } else if (error.message.includes('Failed to fetch') || error.message.includes('NetworkError')) {
        errorMessage += 'Не удалось подключиться к серверу.'
      } else {
        errorMessage += error.message || 'Произошла неизвестная ошибка'
      }

      setError(errorMessage)

      // Автоматически скрыть ошибку через 5 секунд
      setTimeout(() => setError(null), 5000)
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    startNewGame()
  }, [])

  return (
    <div className="app">
      <ErrorMessage message={error} onClose={() => setError(null)} />

      <div className="app-container">
        <h1 className="app-title">✨ Крестики-нолики ✨</h1>

        <div className="telegram-section">
          {!chatId && (
            <div className="chat-id-input">
              <label>📱 Для получения уведомлений в Telegram:</label>
              <a
                href="https://t.me/TicTacToeforDiscountBot?start=game"
                target="_blank"
                rel="noopener noreferrer"
                className="telegram-bot-link"
              >
                ✨ Активировать Telegram-бота ✨
              </a>
              <p className="telegram-instruction">
                1. Нажмите на кнопку выше, чтобы открыть бота<br />
                2. Нажмите "Start" или отправьте команду /start<br />
                3. Бот отправит вам ваш Chat ID - скопируйте его<br />
                4. Вставьте Chat ID в поле ниже<br />
                <span style={{ color: 'var(--primary-pink)', fontWeight: 'bold' }}>💡 Не волнуйтесь, это нужно сделать только один раз! После первого ввода Chat ID сохранится автоматически 😊</span>
              </p>
              <input
                type="text"
                value={chatId}
                onChange={(e) => {
                  const value = e.target.value
                  setChatId(value)
                  localStorage.setItem('chatId', value)
                }}
                placeholder="Ваш Chat ID (например: 850850290)"
              />
              <small>💡 Получите Chat ID через бота (команда /start) или через @userinfobot</small>
            </div>
          )}
          {chatId && (
            <div className="telegram-active">
              <p>✅ Telegram-бот подключен!</p>
              <a
                href="https://t.me/TicTacToeforDiscountBot?start=game"
                target="_blank"
                rel="noopener noreferrer"
                className="telegram-bot-link-small"
              >
                Открыть бота в Telegram
              </a>
            </div>
          )}
        </div>

        <GameBoard
          board={board}
          onCellClick={makeMove}
          disabled={gameStatus !== 'playing' || loading}
        />

        {loading && (
          <div className="loading-indicator">
            <p>Загрузка...</p>
          </div>
        )}

        {gameStatus === 'playing' && (
          <p className="game-status">Ваш ход! Вы играете за ✨</p>
        )}
      </div>

      {showPromoModal && promocode && (
        <PromoCodeModal
          promocode={promocode}
          onClose={() => {
            setShowPromoModal(false)
            startNewGame()
          }}
          onPlayAgain={startNewGame}
        />
      )}

      {showGameOverModal && (
        <GameOverModal
          message={gameMessage}
          onPlayAgain={startNewGame}
        />
      )}
    </div>
  )
}

export default App


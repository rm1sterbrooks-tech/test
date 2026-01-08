import React from 'react'
import './GameBoard.css'

const GameBoard = ({ board, onCellClick, disabled }) => {
  const getSymbol = (cell) => {
    if (cell === 'X') return '✨'
    if (cell === 'O') return '💫'
    return ''
  }

  return (
    <div className="game-board">
      {board.map((row, i) => (
        <div key={i} className="board-row">
          {row.map((cell, j) => (
            <button
              key={j}
              className={`board-cell ${cell ? 'filled' : ''} ${disabled ? 'disabled' : ''}`}
              onClick={() => !disabled && !cell && onCellClick(i, j)}
              disabled={disabled || cell !== ''}
            >
              {getSymbol(cell)}
            </button>
          ))}
        </div>
      ))}
    </div>
  )
}

export default GameBoard


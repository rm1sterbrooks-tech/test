import React from 'react'
import './Modal.css'

const PromoCodeModal = ({ promocode, onClose, onPlayAgain }) => {
  const copyToClipboard = () => {
    navigator.clipboard.writeText(promocode)
    alert('Промокод скопирован!')
  }

  return (
    <div className="modal-overlay">
      <div className="modal-content promo-modal">
        <div className="modal-header">
          <h2>🎉 Поздравляем с победой! 🎉</h2>
        </div>
        <div className="modal-body">
          <p className="promo-label">Ваш промокод на скидку:</p>
          <div className="promocode-display" onClick={copyToClipboard}>
            <span className="promocode">{promocode}</span>
            <span className="copy-hint">(нажмите, чтобы скопировать)</span>
          </div>
        </div>
        <div className="modal-footer">
          <button className="btn-primary" onClick={onPlayAgain}>
            Играть снова ✨
          </button>
          <button className="btn-secondary" onClick={onClose}>
            Закрыть
          </button>
        </div>
      </div>
    </div>
  )
}

export default PromoCodeModal


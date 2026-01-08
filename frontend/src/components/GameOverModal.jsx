import React from 'react'
import './Modal.css'

const GameOverModal = ({ message, onPlayAgain }) => {
  return (
    <div className="modal-overlay">
      <div className="modal-content game-over-modal">
        <div className="modal-header">
          <h2>{message}</h2>
        </div>
        <div className="modal-body">
          <p>Хотите попробовать ещё раз?</p>
        </div>
        <div className="modal-footer">
          <button className="btn-primary" onClick={onPlayAgain}>
            Играть снова ✨
          </button>
        </div>
      </div>
    </div>
  )
}

export default GameOverModal


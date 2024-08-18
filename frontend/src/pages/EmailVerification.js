import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { useLocation, useNavigate } from 'react-router-dom';
import Modal from '@mui/material/Modal'; // Import Modal component
import '../components/EmailVerification.css'; // Ensure this CSS file exists

function EmailVerification() {
  const [code, setCode] = useState(Array(6).fill(''));
  const [timeLeft, setTimeLeft] = useState(300);
  const [canResend, setCanResend] = useState(false);
  const [errorMessage, setErrorMessage] = useState('');
  const [showModal, setShowModal] = useState(false); // Modal visibility state
  const [modalContent, setModalContent] = useState(''); // Modal content
  const location = useLocation();
  const navigate = useNavigate();
  const email = location.state.email;

  useEffect(() => {
    const timer = setInterval(() => {
      setTimeLeft((prevTime) => {
        if (prevTime > 1) {
          return prevTime - 1;
        } else {
          setCanResend(true);
          clearInterval(timer);
          return 0;
        }
      });
    }, 1000);

    return () => clearInterval(timer);
  }, []);

  const handleVerify = () => {
    axios.post('http://localhost:5000/verify-email', {
      email,
      code: code.join('')
    }).then(response => {
      setModalContent(response.data.message);
      setShowModal(true);
      if (response.data.message === 'Email verified successfully.') {
        // Redirect to login or another page after closing modal
        setTimeout(() => {
          setShowModal(false);
          navigate('/login');
        }, 2000);
      }
    }).catch(error => {
      console.error("There was an error verifying the email!", error);
      setModalContent('There was an error verifying the email. Please try again.');
      setShowModal(true);
    });
  };

  const handleResend = () => {
    axios.post('http://localhost:5000/resend-verification', {
      email
    }).then(response => {
      setModalContent(response.data.message);
      setShowModal(true);
      if (response.data.message === 'Verification code resent successfully.') {
        setTimeLeft(300);
        setCanResend(false);
        setErrorMessage('');
      }
    }).catch(error => {
      console.error("There was an error resending the verification code!", error);
      setModalContent('There was an error resending the verification code. Please try again.');
      setShowModal(true);
    });
  };

  const minutes = Math.floor(timeLeft / 60);
  const seconds = timeLeft % 60;

  const handleInputChange = (e, i) => {
    const newCode = [...code];
    newCode[i] = e.target.value;
    setCode(newCode);
    if (e.target.value !== '' && i < 5) {
      document.getElementById(`code-input-${i + 1}`).focus();
    }
  };

  const handleCloseModal = () => {
    setShowModal(false);
  };

  return (
    <div className="verification-container">
      <h2>E-MAIL VERIFICATION</h2>
      {errorMessage && <p className="error-message">{errorMessage}</p>}
      <p>To complete your registration, please enter the code sent to your email in the verification field.</p>
      <div className="code-inputs">
        {code.map((value, i) => (
          <input 
            key={i} 
            id={`code-input-${i}`} 
            type="text" 
            maxLength="1" 
            value={value} 
            onChange={(e) => handleInputChange(e, i)}
            onKeyDown={(e) => {
              if (e.key === 'Backspace' && i > 0 && code[i] === '') {
                document.getElementById(`code-input-${i - 1}`).focus();
              }
            }} 
          />
        ))}
      </div>
      <div className="button-container">
        <button onClick={handleResend} disabled={!canResend} className={!canResend ? 'disabled' : 'resend-button'}>
          Resend Code
        </button>
        <button onClick={handleVerify}>Verify</button>
      </div>
      <div className="timer-container">
        <div className="timer-bar">
          <div className="timer-bar-fill" style={{ width: `${(timeLeft / 300) * 100}%` }}>
            <span className="timer-text">{minutes}:{seconds < 10 ? `0${seconds}` : seconds}</span>
          </div>
        </div>
      </div>

      {/* Modal for displaying messages */}

      <Modal
        open={showModal}
        onClose={handleCloseModal}
        aria-labelledby="modal-title"
        aria-describedby="modal-description"
      >
        <div className="modal-overlay">
          <div className="modal-content">
            <h2 id="modal-title">Notice</h2>
            <p id="modal-description">{modalContent}</p>
            <button onClick={handleCloseModal}>Close</button>
          </div>
        </div>
      </Modal>

    </div>
  );
}

export default EmailVerification;

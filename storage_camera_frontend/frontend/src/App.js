import React, { useState, useEffect } from "react";
import axios from "axios";
import styled from "styled-components";

// Создаём стилизованные компоненты
const AppContainer = styled.div`
  text-align: center;
  margin-top: 50px;
`;

const Title = styled.h1`
  color: #333;
`;

const PasswordInput = styled.input`
  padding: 5px;
  font-size: 16px;
`;

const Button = styled.button`
  margin: 5px;
  padding: 10px 20px;
  font-size: 16px;
  background-color: #007bff;
  color: #fff;
  border: none;
  border-radius: 5px;
  cursor: pointer;

  &:hover {
    background-color: #0056b3;
  }
`;

//Основная функция приложения
function App() {
  const [password, setPassword] = useState("");
  const [message, setMessage] = useState("");

  const handleUnlock = () => {                  // Обработчик события для кнопки "Unlock" (Открыть дверь)
    axios
      .post("http://localhost:5000/unlock", { password })
      .then((response) => {
        setMessage(response.data.message);
      })
      .catch((_error) => {
        setMessage("Error: Incorrect password");
      });
  };

  const handleLock = () => {                     // Обработчик события для кнопки "Lock" (Закрыть дверь)
    axios
      .post("http://localhost:5000/lock")
      .then((response) => {
        setMessage(response.data.message);
      })
      .catch((_error) => {
        setMessage("Error: Door is already locked");
      });
  };

  useEffect(() => {                         // Проверка состояние двери каждые 5 секунд
    const interval = setInterval(() => {
      axios
        .get("http://localhost:5000/state")
        .then((response) => {
          if (response.data.state === "unlocked") {
            setMessage("Warning: Door has been open for more than 5 seconds!");
          } else {
            setMessage("");
          }
        })
        .catch((error) => {
          console.log(error);
        });
    }, 5000);

    return () => clearInterval(interval);
  }, []);

  return (                                         // Код страницы
    <AppContainer>
      <Title>Storage Camera Control</Title>
      <div>
        <label>Password:</label>
        <PasswordInput
          type="password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
        />
      </div>
      <div style={{ margin: "20px" }}>
        <Button onClick={handleUnlock}>Unlock</Button>
        <Button onClick={handleLock}>Lock</Button>
      </div>
      <div>{message}</div>
    </AppContainer>
  );
}

export default App;

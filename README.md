Русский
# Веб-платформа мониторинга макроэкономических, геополитических показателей и ликвидности в блокчейне

Количественная панель финансового анализа

Этот репозиторий содержит полную автоматизированную экосистему для анализа рынков, включая пользовательский интерфейс, API и агенты извлечения данных.

Примечание: В графическом интерфейсе вы увидите 2 пустых окна: Solana ML Prediction и LLM market sentiment. Это связано с тем, что они являются частью другого этапа исследования BKP.

 Инструкции по запуску для преподавателя

Этот проект был упакован с использованием контейнерных технологий (Docker), чтобы гарантировать его идеальную работу в любой среде без необходимости настройки локальных зависимостей.

1. Предварительные требования

Необходимо установить Docker Desktop и убедиться, что ядро Docker запущено.
Примечание: Локальная установка Python, Node.js или баз данных не требуется.

2. Развертывание архитектуры

2.1 Клонируйте этот репозиторий на свой локальный компьютер.

2.2 Откройте терминал (CMD, PowerShell или Terminal) в корневой папке проекта solana-dashboard.

2.3 Выполните следующую команду для сборки и запуска контейнеров:

docker compose up --build


Система автоматически скачает образы и создаст изолированные среды. Этот процесс может занять пару минут при первом запуске.

3. Визуализация проекта

Как только терминал покажет, что сервисы активны, откройте веб-браузер.

 Примечание о сетях и VPN:
Держите VPN включенным, чтобы внешние виджеты загружались корректно.

Получите доступ по следующим ссылкам:

Панель управления (Frontend React): http://127.0.0.1:5173 (Не открывать Localhost:5173)

Интерактивный API (Backend FastAPI): http://127.0.0.1:8000/docs

4. Выключение системы

Чтобы безопасно остановить все контейнеры, вернитесь в терминал, где запущен проект, и нажмите Ctrl + C.


# English

# A web platform for monitoring macroeconomic, geopolitical, and blockchain liquidity indicators.


This repository contains the complete automated ecosystem for market analysis, including the user interface, the API, and the data extraction agents.

Note: In the graphical interface you will observe 2 empty windows, the Solana ML Prediction and LLM market sentiment. This is because they are part of another stage of the BKP research.

 Execution Instructions for the Professor

This project has been packaged using container technology (Docker) to ensure it works perfectly in any environment without the need to configure local dependencies.

1. Prerequisites

It is essential to have Docker Desktop installed and ensure that the Docker engine is running.
Note: Local installation of Python, Node.js, or databases is not required.

2. Architecture Deployment

2.1 Clone this repository to your local machine.

2.2 Open a terminal (CMD, PowerShell, or Terminal) in the project's root folder solana-dashboard.

2.3 Execute the following command to build and start the containers:

docker compose up --build


The system will download the images and build the isolated environments automatically. This process may take a couple of minutes the first time.

3. Project Visualization

Once the terminal indicates that the services are active, open your web browser.

 Note on Networks and VPNs:
Keep the VPN active so that external widgets load correctly.

Access via the following links:

Control Panel (Frontend React): http://127.0.0.1:5173 (Do not open Localhost:5173)

Interactive API (Backend FastAPI): http://127.0.0.1:8000/docs

4. System Shutdown

To safely stop all containers, return to the terminal where the project is running and press
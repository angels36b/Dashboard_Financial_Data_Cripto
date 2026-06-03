import { useEffect, useRef } from 'react';
import { createChart } from 'lightweight-charts';

const TradingChart = () => {
    // Referencias para el contenedor HTML y para guardar la instancia del gráfico
    const chartContainerRef = useRef();
    const chartInstance = useRef(null);

    useEffect(() => {
        // 1. Inicializar el gráfico
        const chart = createChart(chartContainerRef.current, {
            layout: { background: { type: 'solid', color: '#1e1e1e' }, textColor: '#d1d4dc' },
            grid: { vertLines: { color: '#2b2b43' }, horzLines: { color: '#2b2b43' } },
            width: chartContainerRef.current.clientWidth,
            height: 400,
        });
        
        chartInstance.current = chart;
        const candleSeries = chart.addCandlestickSeries();

        // 2. Conectar al WebSocket de Binance
        const ws = new WebSocket('wss://stream.binance.com:9443/ws/solusdt@kline_1m');

        ws.onmessage = (event) => {
            const message = JSON.parse(event.data);
            const candlestick = message.k;

            // Actualizar la serie con el nuevo dato
            candleSeries.update({
                time: candlestick.t / 1000,
                open: parseFloat(candlestick.o),
                high: parseFloat(candlestick.h),
                low: parseFloat(candlestick.l),
                close: parseFloat(candlestick.c)
            });
        };

        // 3. Limpieza y manejo de redimensionamiento
        const handleResize = () => {
            chart.applyOptions({ width: chartContainerRef.current.clientWidth });
        };
        window.addEventListener('resize', handleResize);

        // Esta función se ejecuta si el componente se destruye (el usuario cambia de página)
        return () => {
            window.removeEventListener('resize', handleResize);
            ws.close(); // ¡CRÍTICO PARA EL RENDIMIENTO!
            chart.remove();
        };
    }, []); // El array vacío asegura que esto corra solo una vez al montar el componente

    return (
        <div 
            ref={chartContainerRef} 
            style={{ width: '100%', height: '400px' }} 
        />
    );
};

export default TradingChart;
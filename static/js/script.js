// Основные переменные
let currentTicker = "MSFT";

// Загрузка данных и отрисовка графика
function loadData(ticker) {
    const csvFile = `/data/${ticker}_2024-01-01_2024-06-30.csv`;

    d3.csv(csvFile).then(data => {
        // Преобразование данных
        const parsedData = data.map(d => ({
            date: new Date(d.Date),
            open: +d.Open,
            high: +d.High,
            low: +d.Low,
            close: +d.Close,
            volume: +d.Volume
        }));

        drawChart(parsedData);
    }).catch(error => {
        console.error("Error loading data:", error);
        alert("Ошибка загрузки данных. Проверьте консоль для деталей.");
    });
}

// Отрисовка графика
function drawChart(data) {
    const margin = { top: 20, right: 30, bottom: 50, left: 60 };
    const width = 1000 - margin.left - margin.right;
    const height = 500 - margin.top - margin.bottom;

    // Очищаем предыдущий график
    d3.select("#chart").html("");

    // Создаем SVG
    const svg = d3.select("#chart")
        .append("svg")
        .attr("width", width + margin.left + margin.right)
        .attr("height", height + margin.top + margin.bottom)
        .append("g")
        .attr("transform", `translate(${margin.left},${margin.top})`);

    // Шкалы
    const x = d3.scaleTime()
        .domain(d3.extent(data, d => d.date))
        .range([0, width]);

    const y = d3.scaleLinear()
        .domain([d3.min(data, d => d.low) * 0.95, d3.max(data, d => d.high) * 1.05])
        .range([height, 0]);

    // Оси
    svg.append("g")
        .attr("transform", `translate(0,${height})`)
        .call(d3.axisBottom(x));

    svg.append("g")
        .call(d3.axisLeft(y));

    // Линия цены закрытия
    const line = d3.line()
        .x(d => x(d.date))
        .y(d => y(d.close));

    svg.append("path")
        .datum(data)
        .attr("class", "line")
        .attr("d", line);

    // Название графика
    svg.append("text")
        .attr("x", width / 2)
        .attr("y", -5)
        .attr("text-anchor", "middle")
        .style("font-size", "16px")
        .text(`${currentTicker} - Цена закрытия`);
}

// Обработчики событий
document.getElementById("ticker-select").addEventListener("change", function() {
    currentTicker = this.value;
    loadData(currentTicker);
});

document.getElementById("update-btn").addEventListener("click", function() {
    loadData(currentTicker);
});

// Первоначальная загрузка
loadData(currentTicker);
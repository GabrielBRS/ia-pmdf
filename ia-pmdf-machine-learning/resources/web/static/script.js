document.getElementById('processBtn').addEventListener('click', async () => {
    const file = document.getElementById('fileInput').files[0];
    if (!file) return alert("Insira uma evidência para análise!");

    const output = document.getElementById('output');
    output.style.display = 'block';
    output.innerHTML = "<em>[SISTEMA ORTZION] Executando Deep Learning...</em>";

    const formData = new FormData();
    formData.append('file', file);

    try {
        const response = await fetch('/api/v1/analisar-evidencia', {
            method: 'POST',
            body: formData
        });
        const data = await response.json();

        const statusCor = data.alerta ? "#c0392b" : "#27ae60";
        output.style.borderLeftColor = statusCor;

        output.innerHTML = `
            <strong>PROCESSO:</strong> [INTELIGÊNCIA RODOVIÁRIA]<br>
            <strong>PLACA DETECTADA (LPR):</strong> \${data.lpr.placa}<br>
            <strong>CONFIANÇA OCR:</strong> \${data.lpr.confianca}%<br>
            <hr>
            <strong>MATCH BIOMÉTRICO:</strong> \${data.biometria.similaridade}%<br>
            <strong>STATUS:</strong> \${data.status_veiculo}
        `;
    } catch (err) {
        output.innerHTML = "[ERRO] Falha crítica no motor de inferência Python.";
    }
});
const botaoFinalizar = document.getElementById("finalizar-quiz");
const resultado = document.getElementById("quiz-resultado");

if (botaoFinalizar) {
    botaoFinalizar.addEventListener("click", () => {
        const perguntas = [
            { nome: "q1", correta: "lobo-guara" },
            { nome: "q2", correta: "pequi" },
            { nome: "q3", correta: "veredas" }
        ];

        let acertos = 0;

        perguntas.forEach((pergunta) => {
            const resposta = document.querySelector(`input[name="${pergunta.nome}"]:checked`);
            if (resposta && resposta.value === pergunta.correta) {
                acertos += 1;
            }
        });

        resultado.textContent = `Você acertou ${acertos} de ${perguntas.length} perguntas!`;
    });
}

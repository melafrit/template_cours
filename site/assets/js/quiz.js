/* =================================================================
   quiz.js — Moteur de quiz de chapitre (auto-évaluation)
   Cours "Réglementation des données et conformité" — M. EL AFRIT (CC BY-NC-SA 4.0)
   Usage :
     new QuizEngine('id-conteneur', [
       { question:'…', options:['A','B','C','D'], correct:1, explanation:'…' }, …
     ]);
   ================================================================= */

class QuizEngine {
  constructor(containerId, questions) {
    this.container = document.getElementById(containerId);
    this.questions = questions || [];
    this.index = 0;
    this.answers = new Array(this.questions.length).fill(null);
    if (this.container) this.render();
  }

  render() {
    const q = this.questions[this.index];
    if (!q) return;
    const answered = this.answers[this.index];
    const letters = ['A', 'B', 'C', 'D', 'E', 'F'];

    let opts = '';
    q.options.forEach((opt, i) => {
      let cls = 'quiz-option';
      if (answered !== null) {
        if (i === q.correct) cls += ' correct';
        else if (i === answered) cls += ' incorrect';
      }
      opts += `<button class="${cls}" data-i="${i}" ${answered !== null ? 'disabled' : ''}>
        <span class="opt-letter">${letters[i]}</span><span>${opt}</span></button>`;
    });

    const explain = answered !== null
      ? `<div class="quiz-explanation show"><strong>${answered === q.correct ? '✅ Bonne réponse.' : '❌ Réponse incorrecte.'}</strong> ${q.explanation || ''}</div>`
      : '';

    const score = this.answers.filter((a, i) => a !== null && a === this.questions[i].correct).length;
    const done = this.answers.every(a => a !== null);

    this.container.className = 'quiz-engine';
    this.container.innerHTML = `
      <div class="quiz-engine-head">
        <span class="ico">🧠</span>
        <h3>Quiz express — vérifiez vos acquis</h3>
        <span class="quiz-progress">Question ${this.index + 1} / ${this.questions.length}</span>
      </div>
      <div class="quiz-question">${q.question}</div>
      <div class="quiz-options">${opts}</div>
      ${explain}
      <div class="quiz-actions">
        <button class="btn btn-ghost" data-act="prev" ${this.index === 0 ? 'disabled' : ''}>← Précédent</button>
        <button class="btn btn-primary" data-act="next" ${this.index === this.questions.length - 1 ? 'disabled' : ''}>Suivant →</button>
        ${done ? `<span class="quiz-result">Score : ${score} / ${this.questions.length}</span>` : ''}
      </div>`;

    this.container.querySelectorAll('.quiz-option').forEach(btn => {
      btn.addEventListener('click', () => {
        if (this.answers[this.index] !== null) return;
        this.answers[this.index] = parseInt(btn.dataset.i, 10);
        this.render();
      });
    });
    this.container.querySelector('[data-act="prev"]').addEventListener('click', () => { if (this.index > 0) { this.index--; this.render(); } });
    this.container.querySelector('[data-act="next"]').addEventListener('click', () => { if (this.index < this.questions.length - 1) { this.index++; this.render(); } });
  }
}
window.QuizEngine = QuizEngine;

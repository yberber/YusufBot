import streamlit as st

st.set_page_config(page_title="CV – Yusuf Berber", page_icon="📄", layout="centered")

# Hide the auto-generated sidebar page list
st.markdown("""
<style>
[data-testid="stSidebarNav"] { display: none; }
</style>
""", unsafe_allow_html=True)

st.page_link("app.py", label="💬 Back to Chat", use_container_width=False)

st.markdown("""
<style>
/* ── Reset & base ───────────────────────────────── */
.cv { font-family: "Source Sans Pro", "Helvetica Neue", Arial, sans-serif;
      color: #1a1a2e; line-height: 1.6; max-width: 760px; margin: 0 auto; }

/* ── Header card ────────────────────────────────── */
.cv-header {
  background: linear-gradient(135deg, #0f2b4a 0%, #1a4f8a 100%);
  color: white; padding: 36px 40px 28px; border-radius: 14px;
  margin-bottom: 28px; text-align: center;
}
.cv-header h1 {
  font-size: 2.4em; font-weight: 800; letter-spacing: 3px;
  margin: 0 0 6px; text-transform: uppercase;
}
.cv-header .role {
  font-size: 1.05em; opacity: .85; letter-spacing: 1px; margin-bottom: 18px;
}
.cv-header .links a {
  color: #a8d4ff; text-decoration: none; font-weight: 600;
  font-size: .9em; margin: 0 10px;
}
.cv-header .links a:hover { color: white; text-decoration: underline; }

/* ── Section title ──────────────────────────────── */
.section-title {
  font-size: .8em; font-weight: 800; letter-spacing: 3px;
  text-transform: uppercase; color: #1a4f8a;
  border-bottom: 2px solid #1a4f8a; padding-bottom: 5px;
  margin: 30px 0 16px;
}

/* ── Summary ────────────────────────────────────── */
.summary { font-size: .97em; color: #333; }

/* ── Timeline cards ─────────────────────────────── */
.card {
  border-left: 4px solid #1a4f8a; background: #f4f8ff;
  border-radius: 0 10px 10px 0; padding: 14px 20px;
  margin-bottom: 14px;
}
.card-header { display: flex; justify-content: space-between;
               align-items: flex-start; flex-wrap: wrap; gap: 6px; }
.card-org { font-weight: 700; font-size: 1.03em; color: #0f2b4a; }
.card-loc { font-size: .82em; color: #666; margin-top: 2px; }
.card-role { color: #1a4f8a; font-style: italic; font-size: .94em;
             margin: 4px 0 8px; }
.date-badge {
  background: #ddeeff; color: #1a4f8a; padding: 3px 10px;
  border-radius: 12px; font-size: .78em; font-weight: 700;
  white-space: nowrap;
}
.card ul { margin: 6px 0 0 0; padding-left: 18px; }
.card li { font-size: .88em; color: #333; margin-bottom: 4px; }
.card-grade { display: inline-block; background: #0f2b4a; color: #fff;
              padding: 2px 10px; border-radius: 10px;
              font-size: .78em; font-weight: 700; margin-top: 6px; }

/* ── Project cards ──────────────────────────────── */
.proj-card {
  border: 1px solid #dce6f7; border-radius: 10px;
  padding: 14px 18px; margin-bottom: 12px;
  background: #fafcff;
}
.proj-title { font-weight: 700; color: #0f2b4a; font-size: .97em; }
.proj-year  { color: #888; font-size: .82em; margin-left: 8px; }
.proj-body  { font-size: .87em; color: #444; margin: 6px 0; }
.proj-link  { font-size: .8em; color: #1a4f8a; text-decoration: none; }
.proj-link:hover { text-decoration: underline; }
.sota-badge {
  display: inline-block; background: #e6f9ee; color: #1e7e34;
  border: 1px solid #b2dfcc; padding: 1px 8px; border-radius: 10px;
  font-size: .75em; font-weight: 700; margin-left: 6px;
}

/* ── Skill tags ─────────────────────────────────── */
.skill-group { margin-bottom: 10px; }
.skill-group-label {
  font-size: .78em; font-weight: 700; color: #666;
  text-transform: uppercase; letter-spacing: 1px;
  display: inline-block; width: 140px; vertical-align: top;
  padding-top: 4px;
}
.tags { display: inline-block; }
.tag {
  display: inline-block; padding: 3px 11px; border-radius: 14px;
  font-size: .82em; font-weight: 600; margin: 3px 4px 3px 0;
  background: #e8f0fe; color: #1a4f8a;
}
.tag.expert { background: #0f2b4a; color: #fff; }

/* ── Language badges ────────────────────────────── */
.lang-row { margin-bottom: 8px; display: flex; align-items: center; gap: 10px; }
.lang-name { font-weight: 700; width: 90px; font-size: .92em; }
.lang-level {
  padding: 3px 14px; border-radius: 14px; font-size: .82em; font-weight: 700;
}
.lang-native  { background: #0f2b4a; color: #fff; }
.lang-c2      { background: #1a4f8a; color: #fff; }
.lang-c1      { background: #ddeeff; color: #1a4f8a; }
.lang-desc    { font-size: .82em; color: #666; }
</style>

<div class="cv">

<!-- ── HEADER ──────────────────────────────────────────── -->
<div class="cv-header">
  <h1>Yusuf Berber</h1>
  <div class="role">Data Scientist &nbsp;·&nbsp; Software Engineer</div>
  <div class="links">
    <a href="https://www.linkedin.com/in/yusuf-sancar-berber-66b7a7353/" target="_blank">🔗 LinkedIn</a>
    <a href="https://github.com/yberber" target="_blank">🐙 GitHub</a>
  </div>
</div>

<!-- ── SUMMARY ─────────────────────────────────────────── -->
<div class="section-title">About</div>
<p class="summary">
M.Sc. Data and Computer Science student at Heidelberg University (grade 1.3) with a B.Sc. in Software
Engineering from Heilbronn University (grade 1.4). Hands-on industry experience building LLM-powered
applications and data pipelines, including publishing an official open-source LangChain integration at SAP SE.
Master's thesis achieved State-of-the-Art performance on benchmark emotion-recognition datasets by combining
fine-tuned LLMs with RAG. Fluent in Turkish, German (C2), and English (C1/C2).
</p>

<!-- ── EXPERIENCE ─────────────────────────────────────── -->
<div class="section-title">Experience</div>

<div class="card">
  <div class="card-header">
    <div>
      <div class="card-org">SAP SE</div>
      <div class="card-loc">Walldorf, Germany</div>
    </div>
    <span class="date-badge">Nov 2024 – May 2025</span>
  </div>
  <div class="card-role">Working Student – Software Engineering</div>
  <ul>
    <li>Built and released <strong>langchain-hana</strong>, the official LangChain integration package for SAP HANA Cloud, enabling vector search and knowledge-graph-backed retrieval in LLM applications.</li>
    <li>Implemented keyword search, in-database embeddings, and graph-based retrieval with full unit-test coverage.</li>
    <li>Automated CI/CD quality gates via GitHub Actions; contributed feature parity upstream to LangChain (Python) and LangChainJS (TypeScript).</li>
  </ul>
</div>

<div class="card">
  <div class="card-header">
    <div>
      <div class="card-org">Vector Informatik GmbH</div>
      <div class="card-loc">Stuttgart, Germany</div>
    </div>
    <span class="date-badge">Mar 2021 – Aug 2022</span>
  </div>
  <div class="card-role">Working Student &amp; Intern – Software Engineering</div>
  <ul>
    <li>Contributed to the <strong>ELEKTRA</strong> process tool for a high-performance automotive software platform.</li>
    <li>Implemented server-side reports and validators in Java; developed client-side features in C#.</li>
    <li>Maintained GUI test suite using Ranorex.</li>
  </ul>
</div>

<!-- ── EDUCATION ──────────────────────────────────────── -->
<div class="section-title">Education</div>

<div class="card">
  <div class="card-header">
    <div>
      <div class="card-org">Heidelberg University</div>
      <div class="card-loc">Heidelberg, Germany</div>
    </div>
    <span class="date-badge">Oct 2023 – Jan 2026</span>
  </div>
  <div class="card-role">M.Sc. Data and Computer Science</div>
  <span class="card-grade">Grade: 1.3 – Very Good</span>
</div>

<div class="card">
  <div class="card-header">
    <div>
      <div class="card-org">Heilbronn University</div>
      <div class="card-loc">Heilbronn, Germany</div>
    </div>
    <span class="date-badge">Mar 2019 – Aug 2023</span>
  </div>
  <div class="card-role">B.Sc. Software Engineering</div>
  <span class="card-grade">Grade: 1.4 – Very Good</span>
</div>

<!-- ── PROJECTS ────────────────────────────────────────── -->
<div class="section-title">Selected Projects</div>

<div class="proj-card">
  <div>
    <span class="proj-title">Emotion Detection in Conversational AI (Master's Thesis)</span>
    <span class="proj-year">2025</span>
    <span class="sota-badge">SOTA</span>
  </div>
  <p class="proj-body">
    Fine-tuned <strong>LLaMA-3.1-8B-Instruct</strong> using two-phase QLoRA with systematic ablations.
    Combined engineered audio features with retrieval-augmented in-context exemplars (RAG) to achieve
    State-of-the-Art performance on the <strong>MELD</strong> and <strong>IEMOCAP</strong> benchmark datasets.
  </p>
  <a class="proj-link" href="https://github.com/yberber/mm-rag-erc" target="_blank">→ github.com/yberber/mm-rag-erc</a>
</div>

<div class="proj-card">
  <div>
    <span class="proj-title">RAGMedAssist – LLM Medical Chatbot</span>
    <span class="proj-year">2023–2024</span>
  </div>
  <p class="proj-body">
    Co-developed an end-to-end LLM-powered medical assistant with retrieval-augmented generation pipelines
    tailored for the medical domain.
  </p>
  <a class="proj-link" href="https://github.com/Matteo-Malve/RAGMedAssist-INLPT-WS2023" target="_blank">→ github.com/Matteo-Malve/RAGMedAssist-INLPT-WS2023</a>
</div>

<div class="proj-card">
  <div>
    <span class="proj-title">AlphaZero for International Checkers (Bachelor's Thesis)</span>
    <span class="proj-year">2023</span>
  </div>
  <p class="proj-body">
    Re-engineered the AlphaZero algorithm using <strong>MCTS</strong> and <strong>ResNets</strong>;
    built a simulation environment to generate synthetic training data via self-play.
  </p>
  <a class="proj-link" href="https://github.com/yberber/Checkers-AI-Minimax-Neural_Network" target="_blank">→ github.com/yberber/Checkers-AI-Minimax-Neural_Network</a>
</div>

<div class="proj-card">
  <div>
    <span class="proj-title">Anime Face Generator Pipeline</span>
    <span class="proj-year">2024</span>
  </div>
  <p class="proj-body">
    GAN-based image generation pipeline using <strong>DCGAN</strong> and <strong>WGAN-GP</strong>
    with PyTorch, combined with <strong>Real-ESRGAN</strong> for high-quality upscaling.
  </p>
  <a class="proj-link" href="https://github.com/yberber/anime-face-gan-pipeline" target="_blank">→ github.com/yberber/anime-face-gan-pipeline</a>
</div>

<!-- ── SKILLS ──────────────────────────────────────────── -->
<div class="section-title">Technical Skills</div>

<div class="skill-group">
  <span class="skill-group-label">Languages</span>
  <span class="tags">
    <span class="tag expert">Python</span>
    <span class="tag expert">Java</span>
    <span class="tag">C / C++</span>
    <span class="tag">C#</span>
    <span class="tag">Go</span>
    <span class="tag">JavaScript</span>
    <span class="tag">TypeScript</span>
  </span>
</div>

<div class="skill-group">
  <span class="skill-group-label">ML / AI</span>
  <span class="tags">
    <span class="tag expert">PyTorch</span>
    <span class="tag expert">LangChain</span>
    <span class="tag">TensorFlow</span>
    <span class="tag">JAX</span>
    <span class="tag">HuggingFace</span>
    <span class="tag">Scikit-learn</span>
    <span class="tag">Pandas</span>
    <span class="tag">Apache Spark</span>
  </span>
</div>

<div class="skill-group">
  <span class="skill-group-label">Infrastructure</span>
  <span class="tags">
    <span class="tag">Docker</span>
    <span class="tag">GitHub Actions</span>
    <span class="tag">Jenkins</span>
    <span class="tag">AWS</span>
    <span class="tag">Linux / Bash</span>
    <span class="tag">Git</span>
    <span class="tag">Flutter</span>
  </span>
</div>

<!-- ── LANGUAGES ──────────────────────────────────────── -->
<div class="section-title">Languages</div>

<div class="lang-row">
  <span class="lang-name">Turkish</span>
  <span class="lang-level lang-native">Native</span>
</div>
<div class="lang-row">
  <span class="lang-name">German</span>
  <span class="lang-level lang-c2">C2 – Proficient</span>
</div>
<div class="lang-row">
  <span class="lang-name">English</span>
  <span class="lang-level lang-c1">C1 / C2 – Proficient</span>
</div>

<br>
</div>
""", unsafe_allow_html=True)

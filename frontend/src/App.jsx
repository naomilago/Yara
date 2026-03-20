import React, { useState, useEffect } from 'react';
import { Routes, Route, Link } from 'react-router-dom';
import { Moon, Sun, Shield, ArrowRight, MessageCircle, Heart, Sparkles, BookOpen } from 'lucide-react';
import logoSrc from './assets/logo.png';

const WhatsAppRedirectUrl = 'https://wa.me/15551425081?text=Oi%20Yara!%20%F0%9F%8C%BA';

const Header = ({ theme, toggleTheme }) => (
  <header className="main-header">
    <div className="header-content max-w-7xl mx-auto flex justify-between items-center w-full">
      <Link to="/" className="logo-section">
        <img src={logoSrc} alt="Yara Logo" className="logo-image" />
        <div className="header-title">
          <h1>Yara</h1>
        </div>
      </Link>
      <div className="header-actions">
        <Link to="/privacidade" className="icon-btn" title="Política de Privacidade">
          <Shield size={20} />
        </Link>
        <button onClick={toggleTheme} className="icon-btn" title="Mudar Tema">
          {theme === 'dark' ? <Sun size={20} /> : <Moon size={20} />}
        </button>
      </div>
    </div>
  </header>
);

const FeatureCard = ({ icon: Icon, title, description }) => (
  <div className="feature-card">
    <div className="feature-icon-wrapper">
      <Icon size={28} className="feature-icon" />
    </div>
    <h3 className="feature-title">{title}</h3>
    <p className="feature-description">{description}</p>
  </div>
);

const LandingPage = () => {
  return (
    <div className="landing-container">
      {/* Hero Section */}
      <section className="hero-section">
        <div className="hero-background">
          <div className="gradient-blob blob-1"></div>
          <div className="gradient-blob blob-2"></div>
          <div className="gradient-blob blob-3"></div>
        </div>
        
        <div className="hero-content">
          <div className="badge">
            <Sparkles size={14} className="badge-icon" />
            <span>Sua nova assistente virtual</span>
          </div>
          <h1 className="hero-headline">
            Acolhimento,<br/>
            <span className="text-gradient">informação e respeito.</span>
          </h1>
          <p className="hero-subtitle">
            Yara é uma inteligência artificial criada exclusivamente para apoiar a 
            comunidade trans e não-binária do Brasil. Prática, segura e disponível 24h.
          </p>
          
          <div className="hero-cta-group">
            <a 
              href={WhatsAppRedirectUrl} 
              target="_blank" 
              rel="noopener noreferrer" 
              className="primary-btn"
            >
              <MessageCircle size={22} />
              Conversar no WhatsApp
            </a>
            <p className="whatsapp-number">+1 (555) 142-5081</p>
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section className="features-section">
        <div className="features-grid">
          <FeatureCard 
            icon={Heart} 
            title="Apoio e Bem-Estar" 
            description="Meditações guiadas, rastreador de humor e um diário de transição seguro e confidencial."
          />
          <FeatureCard 
            icon={BookOpen} 
            title="Direitos e SUS" 
            description="Guia passo a passo para retificação de nome, busca de ambulatórios trans e cartilhas de saúde."
          />
          <FeatureCard 
            icon={MessageCircle} 
            title="Respostas em Áudio" 
            description="Além de texto, a Yara pode conversar por áudios humanizados, trazendo calor e proximidade."
          />
        </div>
      </section>

      {/* Footer */}
      <footer className="landing-footer">
        <p>Criado por e para a comunidade trans. 🏳️‍⚧️</p>
        <Link to="/privacidade" className="footer-link">Política de Privacidade</Link>
      </footer>
    </div>
  );
};

const PrivacyPolicy = () => (
  <div className="page-container privacy-page">
    <Link to="/" className="back-link">
      <ArrowRight className="back-arrow" size={16} /> Voltar
    </Link>
    
    <div className="glass-panel">
      <h1 className="page-title">Privacidade e Segurança</h1>
      
      <div className="privacy-content">
        <p className="lead-text">
          A Yara foi criada para ser um espaço radicalmente seguro para a comunidade trans.
          Sua privacidade é nossa prioridade inegociável.
        </p>

        <div className="privacy-section">
          <h2>Coleta de Dados</h2>
          <p>
            Não solicitamos e nem armazenamos seu nome civil, CPF ou endereço. A proteção do
            seu número de WhatsApp é tratada com total sigilo e usada apenas temporariamente 
            na memória do servidor para manter o contexto se você acessar o Diário ou 
            Rastreamento de Humor (mantemos apenas as últimas 20 mensagens em cache volátil).
          </p>
        </div>

        <div className="privacy-section">
          <h2>Nenhum Treinamento com seus Dados</h2>
          <p>
            A Yara utiliza os modelos em nuvem das maiores empresas de inteligências 
            artificiais fechadas sob uma Política Comercial Estrita; suas conversas
            <strong> jamais</strong> são usadas para treinar modelos abertamente.
          </p>
        </div>

        <div className="privacy-section">
          <h2>Disclaimer Médico e Jurídico</h2>
          <p>
            A Yara é uma assistente de IA. Mesmo que ofereça cartilhas sobre hormonização e
            guias de retificação baseados nas varas do Supremo, <strong>ela não substitui 
            acompanhamento de médicos endocrinologistas ou orientação da Defensoria Pública.</strong>
          </p>
        </div>
      </div>
    </div>
  </div>
);

function App() {
  const [theme, setTheme] = useState('light');

  useEffect(() => {
    // Definir tema inicial
    const savedTheme = localStorage.getItem('yara_theme') || 'light';
    setTheme(savedTheme);
    document.documentElement.setAttribute('data-theme', savedTheme);
  }, []);

  const toggleTheme = () => {
    const newTheme = theme === 'light' ? 'dark' : 'light';
    setTheme(newTheme);
    document.documentElement.setAttribute('data-theme', newTheme);
    localStorage.setItem('yara_theme', newTheme);
  };

  return (
    <div className="app-root">
      <Header theme={theme} toggleTheme={toggleTheme} />
      <Routes>
        <Route path="/" element={<LandingPage />} />
        <Route path="/privacidade" element={<PrivacyPolicy />} />
      </Routes>
    </div>
  );
}

export default App;

import sys
import os
from unittest.mock import MagicMock, patch

# Adiciona o diretório backend ao path para importação
sys.path.append(os.path.join(os.getcwd(), 'backend'))

# Mock constants/settings before imports if needed
with patch('settings.settings') as mock_settings:
    mock_settings.model_name = 'llama-3.1-8b-instant'
    mock_settings.groq_api_key = 'fake-key'
    
    from agent.graph import build_graph
    from whatsapp.handler import handle_message

async def test_trimming():
    print("Testing message trimming...")
    # Mocking ChatGroq to avoid real API calls
    with patch('agent.graph.ChatGroq') as mock_chat:
        mock_llm = MagicMock()
        mock_chat.return_value = mock_llm
        
        graph = build_graph()
        
        # Simula um estado com 15 mensagens
        messages = [{"role": "user", "content": f"msg {i}"} for i in range(15)]
        
        # O state_modifier deve ser chamado internamente pelo graph.invoke ou similar
        # Mas aqui queremos testar o state_modifier diretamente se possível
        # Como ele está definido dentro de build_graph, vamos tentar extraí-lo ou testar via invoke
        
        # Mock do invoke para ver o que ele recebe
        # Na verdade, create_react_agent é complexo. 
        # Vamos testar se o handler chama o graph corretamente.
        pass

async def test_clear_command():
    print("Testing clear command...")
    with patch('whatsapp.handler.send_text') as mock_send:
        with patch('whatsapp.handler.build_graph') as mock_build:
            mock_graph = MagicMock()
            mock_build.return_value = mock_graph
            
            # Testa o comando !limpar
            from handler import handle_message
            await handle_message("12345", "!limpar")
            
            mock_graph.update_state.assert_called_once()
            mock_send.assert_called_with(to="12345", text=patch.any)
            print("Clear command works!")

if __name__ == "__main__":
    # Este é um esboço, rodar testes assíncronos requer mais setup (pytest-asyncio)
    # Vou fazer uma verificação manual da lógica nos arquivos.
    print("Test script created. Logic remains to be verified via execution if possible.")

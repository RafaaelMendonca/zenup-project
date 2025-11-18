import sqlite3
import json
import logging
from typing import List, Dict, Optional

logger = logging.getLogger(__name__)

class SQLiteModel:
    """
    Modelo de dados para gerenciar conversas usando SQLite.
    Cada mensagem é armazenada em uma tabela 'mensagens'.
    """
    def __init__(self, db_path: str = 'conversas.db'):
        """
        Inicializa a conexão com o banco de dados e garante que a tabela existe.
        :param db_path: Caminho para o arquivo do banco de dados SQLite.
        """
        self.db_path = db_path
        self._inicializar_banco()

    def _get_conexao(self) -> sqlite3.Connection:
        """ Cria e retorna uma nova conexão com o banco de dados. """
        return sqlite3.connect(self.db_path)

    def _inicializar_banco(self):
        """ Cria a tabela 'mensagens' se ela não existir. """
        try:
            conn = self._get_conexao()
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS mensagens (
                    id_usuario INTEGER NOT NULL,
                    role TEXT NOT NULL,
                    mensagem TEXT NOT NULL,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
                );
            """)
            conn.commit()
            conn.close()
        except sqlite3.Error as e:
            logger.error(f"Erro ao inicializar o banco de dados SQLite: {e}")

    def verificacao_sqlite(self) -> bool:
        try:
            conn = self._get_conexao()
            conn.close()
            return True
        except sqlite3.Error as e:
            logger.error(f"Erro de conexão/verificação do SQLite: {e}")
            return False

    def salvar_mensagem(self, id_usuario: int, role: str, mensagem: str) -> bool:
        """
        Salva uma nova mensagem no banco de dados.
        :param id_usuario: ID do usuário a quem a mensagem pertence.
        :param role: O papel (e.g., 'user', 'system', 'assistant').
        :param mensagem: O conteúdo da mensagem.
        :return: True se a mensagem foi salva com sucesso, False caso contrário.
        """
        try:
            conn = self._get_conexao()
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO mensagens (id_usuario, role, mensagem) VALUES (?, ?, ?)",
                (id_usuario, role, mensagem)
            )
            conn.commit()
            conn.close()
            return True
        except sqlite3.Error as e:
            logger.error(f"Erro ao salvar mensagem no SQLite: {e}")
            return False

    def buscar_conversa(self, id_usuario: int) -> List[Dict[str, str]]:
        """
        Busca todas as mensagens para um determinado id_usuario, ordenadas por timestamp.
        :param id_usuario: ID do usuário.
        :return: Uma lista de dicionários, cada um representando uma mensagem.
        """
        conversa = []
        try:
            conn = self._get_conexao()
            cursor = conn.cursor()
            cursor.execute(
                "SELECT role, mensagem FROM mensagens WHERE id_usuario = ? ORDER BY timestamp ASC",
                (id_usuario,)
            )
            
            # Mapeia os resultados da consulta para o formato {"role": role, "content": mensagem}
            for role, mensagem in cursor.fetchall():
                conversa.append({"role": role, "content": mensagem})
                
            conn.close()
            return conversa
        except sqlite3.Error as e:
            logger.error(f"Erro ao buscar conversa no SQLite: {e}")
            return []

    def limpar_conversa(self, id_usuario: int) -> bool:
        """
        Exclui todas as mensagens associadas a um id_usuario.
        :param id_usuario: ID do usuário cuja conversa deve ser limpa.
        :return: True se a conversa foi limpa com sucesso, False caso contrário.
        """
        try:
            conn = self._get_conexao()
            cursor = conn.cursor()
            cursor.execute(
                "DELETE FROM mensagens WHERE id_usuario = ?", 
                (id_usuario,)
            )
            conn.commit()
            conn.close()
            return True
        except sqlite3.Error as e:
            logger.error(f"Erro ao limpar conversa no SQLite: {e}")
            return False
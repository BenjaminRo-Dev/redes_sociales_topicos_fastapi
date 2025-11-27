"""inserta datos iniciales

Revision ID: 4782d32e1eb1
Revises: f46bb54357e3
Create Date: 2025-11-27 08:45:35.660413

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import bcrypt


# revision identifiers, used by Alembic.
revision: str = '4782d32e1eb1'
down_revision: Union[str, Sequence[str], None] = 'f46bb54357e3'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def get_password_hash(password: str) -> str:
    password_bytes = password.encode('utf-8')
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password_bytes, salt)
    return hashed.decode('utf-8')

def upgrade():
    password_plano = "00000000"
    password_hash = get_password_hash(password_plano)
    op.execute(
        f"INSERT INTO usuario (nombre, email, password, create_at, update_at) VALUES ('Benjamin Romero', 'benjamin@example.com', '{password_hash}', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP)"
    )
    

def downgrade():
    op.execute("DELETE FROM usuario WHERE email = 'benjamin@example.com'")
    
"""insertar datos iniciales

Revision ID: 825d29034768
Revises: 75efcc3576c2
Create Date: 2025-11-12 16:20:19.827566

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import bcrypt

# revision identifiers, used by Alembic.
revision: str = '825d29034768'
down_revision: Union[str, Sequence[str], None] = '75efcc3576c2'
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
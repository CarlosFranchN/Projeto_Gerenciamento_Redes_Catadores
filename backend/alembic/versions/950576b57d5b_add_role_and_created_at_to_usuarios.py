"""add role and created_at to usuarios

Revision ID: 950576b57d5b
Revises: d66031aa8eb1
Create Date: 2026-03-14 15:00:32.530082

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '950576b57d5b'
down_revision: Union[str, Sequence[str], None] = 'd66031aa8eb1'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Adiciona coluna role
    op.add_column('usuarios', sa.Column('role', sa.String(length=20), nullable=True, server_default='admin'))
    
    # Adiciona coluna created_at
    op.add_column('usuarios', sa.Column('created_at', sa.DateTime(), nullable=True))
    
    # Popula role para usuários existentes
    op.execute("UPDATE usuarios SET role = 'admin' WHERE role IS NULL")
    
    # Torna role NOT NULL (opcional)
    op.alter_column('usuarios', 'role', existing_type=sa.String(20), nullable=False)



def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column('usuarios', 'created_at')
    op.drop_column('usuarios', 'role')
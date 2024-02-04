"""adding content column

Revision ID: f2b523006c00
Revises: efa5fe39bd2f
Create Date: 2024-01-30 16:39:53.700363

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'f2b523006c00'
down_revision: Union[str, None] = 'efa5fe39bd2f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('content', sa.String(), nullable=False))
    pass


def downgrade() -> None:
    op.drop_column('posts', 'content')
    pass

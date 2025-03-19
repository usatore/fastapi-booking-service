"""Today is new day

Revision ID: 3da267b0d35d
Revises: cd6599c9d507
Create Date: 2025-02-11 14:42:24.303939

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "3da267b0d35d"
down_revision: Union[str, None] = "cd6599c9d507"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        "bookings",
        sa.Column(
            "total_days",
            sa.Integer(),
            sa.Computed(
                "(date_to - date_from)",
            ),
            nullable=True,
        ),
    )
    op.add_column(
        "bookings",
        sa.Column(
            "total_cost",
            sa.Integer(),
            sa.Computed(
                "((date_to - date_from) * price)",
            ),
            nullable=True,
        ),
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column("bookings", "total_cost")
    op.drop_column("bookings", "total_days")
    # ### end Alembic commands ###

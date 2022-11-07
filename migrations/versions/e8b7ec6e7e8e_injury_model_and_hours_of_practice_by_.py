"""injury model and hours of practice by week field

Revision ID: e8b7ec6e7e8e
Revises: e1d482374bd0
Create Date: 2022-11-06 17:52:52.534162

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e8b7ec6e7e8e'
down_revision = 'e1d482374bd0'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('injury',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('sport_profile_id', sa.Integer(), nullable=True),
    sa.Column('injury_name', sa.Enum('SINDROME_PALETOFEMORAL', 'ROTULA', 'TENDINITIS', 'SINDROME_PLICA_MEDIAL', 'SINDROME_BANDA_ILIOTIBIAL', 'OTRA', 'NINGUNA', 'TORCEDURAS_DISTENSIONES', 'LESIONES_RODILLA', 'INFLAMACION_MUSCULAR', 'TRAUMATISMOS_TENDON_AQUILES', 'DOLOR_HUESO_TIBIA', 'LESIONES_MANGUITO_ROTATORIO', 'FRACTURAS', 'DISLOCACIONES', name='injuryenum'), nullable=True),
    sa.ForeignKeyConstraint(['sport_profile_id'], ['sport_profile.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.add_column('sport_profile', sa.Column('hours_of_practice_by_week', sa.Integer(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('sport_profile', 'hours_of_practice_by_week')
    op.drop_table('injury')
    # ### end Alembic commands ###

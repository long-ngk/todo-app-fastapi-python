"""Create tables and add sample data

Revision ID: 001
Revises: 
Create Date: 2024-01-01 00:00:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy import text

# revision identifiers, used by Alembic.
revision = '001'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Create companies table
    op.create_table('companies',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(), nullable=True),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('mode', sa.String(), nullable=True),
        sa.Column('rating', sa.Integer(), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_companies_id'), 'companies', ['id'], unique=False)
    op.create_index(op.f('ix_companies_name'), 'companies', ['name'], unique=True)

    # Create users table
    op.create_table('users',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('email', sa.String(), nullable=True),
        sa.Column('username', sa.String(), nullable=True),
        sa.Column('first_name', sa.String(), nullable=True),
        sa.Column('last_name', sa.String(), nullable=True),
        sa.Column('hashed_password', sa.String(), nullable=True),
        sa.Column('is_active', sa.Boolean(), nullable=True),
        sa.Column('is_admin', sa.Boolean(), nullable=True),
        sa.Column('company_id', sa.Integer(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.ForeignKeyConstraint(['company_id'], ['companies.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_users_email'), 'users', ['email'], unique=True)
    op.create_index(op.f('ix_users_id'), 'users', ['id'], unique=False)
    op.create_index(op.f('ix_users_username'), 'users', ['username'], unique=True)

    # Create tasks table
    op.create_table('tasks',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('summary', sa.String(), nullable=True),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('status', sa.String(), nullable=True),
        sa.Column('priority', sa.String(), nullable=True),
        sa.Column('user_id', sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_tasks_id'), 'tasks', ['id'], unique=False)
    op.create_index(op.f('ix_tasks_summary'), 'tasks', ['summary'], unique=False)

    # Insert sample data
    op.execute(text("""
        INSERT INTO companies (name, description, mode, rating) VALUES
        ('Tech Corp', 'Technology company', 'hybrid', 5),
        ('StartupXYZ', 'Innovative startup', 'remote', 4),
        ('Enterprise Ltd', 'Large enterprise', 'office', 3);
    """))

    op.execute(text("""
        INSERT INTO users (email, username, first_name, last_name, hashed_password, is_active, is_admin, company_id) VALUES
        ('admin@techcorp.com', 'admin', 'Admin', 'User', '$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW', true, true, 1),
        ('john@techcorp.com', 'john_doe', 'John', 'Doe', '$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW', true, false, 1),
        ('jane@startupxyz.com', 'jane_smith', 'Jane', 'Smith', '$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW', true, false, 2);
    """))

    op.execute(text("""
        INSERT INTO tasks (summary, description, status, priority, user_id) VALUES
        ('Setup project', 'Initialize the FastAPI project', 'completed', 'high', 2),
        ('Create API endpoints', 'Develop REST API endpoints', 'in_progress', 'high', 2),
        ('Write documentation', 'Document the API', 'todo', 'medium', 2),
        ('Design database', 'Create database schema', 'completed', 'high', 3),
        ('Implement authentication', 'Add JWT authentication', 'in_progress', 'high', 3);
    """))


def downgrade() -> None:
    op.drop_index(op.f('ix_tasks_summary'), table_name='tasks')
    op.drop_index(op.f('ix_tasks_id'), table_name='tasks')
    op.drop_table('tasks')
    op.drop_index(op.f('ix_users_username'), table_name='users')
    op.drop_index(op.f('ix_users_id'), table_name='users')
    op.drop_index(op.f('ix_users_email'), table_name='users')
    op.drop_table('users')
    op.drop_index(op.f('ix_companies_name'), table_name='companies')
    op.drop_index(op.f('ix_companies_id'), table_name='companies')
    op.drop_table('companies')
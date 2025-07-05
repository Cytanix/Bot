# Copyright (c) 2025 SpiritTheWalf and Cytanix
#
# This work is licensed under the Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License.
# To view a copy of this license, visit https://creativecommons.org/licenses/by-nc-sa/4.0/ or see the LICENSE file.
# pylint: disable=R0903
"""This file contains the database logic, including the tables and connection data"""
import os
import asyncio
from datetime import datetime as dt, timezone as tz
from dotenv import load_dotenv
from sqlalchemy import Column, BigInteger, String, Boolean, Index, Integer, ForeignKeyConstraint, URL, CheckConstraint
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, AsyncEngine, async_sessionmaker
from sqlalchemy.orm import declarative_base, relationship

load_dotenv()
Base = declarative_base()
connection_url = URL.create(
    "postgresql+asyncpg",
    username=os.getenv("DATABASE_USERNAME"),
    password=os.getenv("DATABASE_PASSWORD"),
    host=os.getenv("DATABASE_HOST"),
    port=os.getenv("DATABASE_PORT"),
    database=os.getenv("DATABASE"),
)
engine: AsyncEngine = create_async_engine(
    connection_url,
    pool_size=10,
    max_overflow=20,
    pool_timeout=30,
    echo=False,)
session_factory = async_sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)

class Logs(Base): # type: ignore
    """Model for the logging table"""
    __tablename__ = 'logs'

    guild_id = Column(BigInteger, primary_key=True, unique=True)
    message_logs = Column(BigInteger)
    member_logs = Column(BigInteger)
    voice_logs = Column(BigInteger)
    mod_logs = Column(BigInteger)
    muterole = Column(BigInteger)
    muterole_channel = Column(BigInteger)
    reaction_logging = Column(BigInteger)

    reg_role = relationship("RegRoles", back_populates="log", uselist=False, cascade="all, delete")


class Punishments(Base): # type: ignore
    """Model for the punishments table"""
    __tablename__ = 'punishments'
    __table_args__ = (
        Index('ix_guild_user_id', 'guild_id', 'user_id'),
    )

    punishment_id = Column(BigInteger, primary_key=True, autoincrement=True)
    guild_id = Column(BigInteger, nullable=False)
    user_id = Column(BigInteger, nullable=False)
    punishment = Column(String, nullable=False)
    punishment_time = Column(BigInteger, nullable=False)  # Will be stored as a unix epoch timestamp
    moderator_id = Column(BigInteger, nullable=False)
    reason = Column(String, default="No reason provided")

class CustomCommands(Base): # type: ignore
    """Model for the custom commands table"""
    __tablename__ = 'custom_commands'

    name = Column(String, primary_key=True)
    owner_id = Column(BigInteger, nullable=False)
    created_at = Column(BigInteger, default=int(dt.now(tz.utc).timestamp())) # Will be stored as a unix epoch timestamp
    text = Column(String)
    image = Column(String) # or LargeBinary, if string the image will be stored base64 encoded
    nsfw = Column(Boolean)

class Registration(Base): # type: ignore
    """Model for the registration table"""
    __tablename__ = 'registrations'
    user_id = Column(BigInteger, primary_key=True)
    gender = Column(String)
    sexuality = Column(String)
    position = Column(String)
    dms = Column(String)
    relationship = Column(String)
    mention = Column(Boolean)
    dob = Column(String)
    registered_at = Column(BigInteger)
    age_verified = Column(Boolean, default=False)
    artist_verified = Column(Boolean, default=False)
    nsfw_lockout = Column(Boolean, default=False)
    artist_lockout = Column(Boolean, default=False)
    nsfw = Column(Boolean, default=False)


class Levels(Base): # type: ignore
    """Model for the levels table"""
    __tablename__ = 'levels'
    __table_args__ = (
        Index('ix_user_guild', 'user_id', 'guild_id'),
        Index('ix_guild', 'guild_id'),
        ForeignKeyConstraint(["user_id"], ["registrations.user_id"], ondelete="CASCADE"),
        ForeignKeyConstraint(["guild_id"], ["logs.guild_id"]),
    )

    guild_id = Column(BigInteger, primary_key=True)
    user_id = Column(BigInteger, primary_key=True)
    level = Column(Integer, default=1, nullable=False)
    xp = Column(BigInteger, default=0, nullable=False)


class RegRoles(Base): # type: ignore
    """Model for the registration roles table"""
    __tablename__ = 'reg_roles'
    __table_args__ = (
        ForeignKeyConstraint(["guild_id"], ["logs.guild_id"]),
    )

    guild_id = Column(BigInteger, primary_key=True)
    registered = Column(BigInteger)
    mention_mention = Column(BigInteger)
    mention_no_mention = Column(BigInteger)
    dms_allowed = Column(BigInteger)
    dms_not_allowed = Column(BigInteger)
    dms_ask = Column(BigInteger)
    gender_male = Column(BigInteger)
    gender_female = Column(BigInteger)
    gender_genderfluid = Column(BigInteger)
    gender_agender = Column(BigInteger)
    gender_non_binary = Column(BigInteger)
    gender_transgender = Column(BigInteger)
    gender_trans_male = Column(BigInteger)
    gender_trans_female = Column(BigInteger)
    relationship_taken = Column(BigInteger)
    relationship_single = Column(BigInteger)
    relationship_single_seeking = Column(BigInteger)
    relationship_single_not = Column(BigInteger)
    relationship_rather_not = Column(BigInteger)
    sexuality_asexual = Column(BigInteger)
    sexuality_bisexual = Column(BigInteger)
    sexuality_gay = Column(BigInteger)
    sexuality_lesbian = Column(BigInteger)
    sexuality_pansexual = Column(BigInteger)
    sexuality_aromantic = Column(BigInteger)
    sexuality_rather_not = Column(BigInteger)
    position_dominant = Column(BigInteger)
    position_submissive = Column(BigInteger)
    position_switch = Column(BigInteger)
    position_rather_not = Column(BigInteger)
    position_neither = Column(BigInteger)

    log = relationship("Logs", back_populates="reg_role")

class BlacklistedUsers(Base):
    """Model for the blacklisted users table"""
    __tablename__ = 'blacklisted_users'
    __table_args__ = (
        CheckConstraint(
            "(is_actively_blacklisted = TRUE) OR (why_unblacklisted IS NOT NULL AND why_unblacklisted != '')",
            name="check_unblacklisted_reason"
        ),
    )
    user_id = Column(BigInteger, primary_key=True)
    date_blacklisted = Column(BigInteger, nullable=False)
    reason = Column(String, nullable=False)
    is_actively_blacklisted = Column(Boolean, default=True)
    date_unblacklisted = Column(BigInteger, nullable=True)
    why_unblacklisted = Column(String, nullable=True)

    def to_dict(self) -> Dict[str, Union[str, int, bool, None]]:
        return {
            "user_id": self.user_id,
            "date_blacklisted": self.date_blacklisted,
            "reason": self.reason,
            "is_actively_blacklisted": self.is_actively_blacklisted,
            "date_unblacklisted": self.date_unblacklisted,
            "why_unblacklisted": self.why_unblacklisted,
        }


async def create_tables() -> None:
    """Create the tables"""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


if __name__ == '__main__':
    asyncio.run(create_tables())

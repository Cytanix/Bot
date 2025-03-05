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
from sqlalchemy import Column, BigInteger, String, Boolean, Index, Integer, ForeignKeyConstraint
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, AsyncEngine
from sqlalchemy.orm import sessionmaker, declarative_base

load_dotenv()
Base = declarative_base()
engine: AsyncEngine = create_async_engine(
    os.getenv("DATABASE_URL"),
    pool_size=10,
    max_overflow=20,
    pool_timeout=30,
    echo=True)
session_factory = sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)

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
    overage = Column(Boolean)
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

class Levels(Base): # type: ignore
    """Model for the levels table"""
    __tablename__ = 'levels'
    __table_args__ = (
        Index('ix_user_guild', 'user_id', 'guild_id'),
        ForeignKeyConstraint(["user_id"], ["registrations.user_id"]),
        ForeignKeyConstraint(["guild_id"], ["logs.guild_id"]),
    )

    user_id = Column(BigInteger, primary_key=True)
    guild_id = Column(BigInteger, primary_key=True)
    level = Column(Integer, default=1)
    xp = Column(BigInteger, default=0)


async def create_tables() -> None:
    """Create the tables"""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


if __name__ == '__main__':
    asyncio.run(create_tables())

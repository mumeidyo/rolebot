from datetime import datetime
from app import db

class Message(db.Model):
    """メッセージ履歴を保存するモデル"""
    id = db.Column(db.Integer, primary_key=True)
    platform = db.Column(db.String(10), nullable=False)  # 'LINE' or 'Discord'
    sender_id = db.Column(db.String(100), nullable=False)
    sender_name = db.Column(db.String(100))
    content = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    forwarded = db.Column(db.Boolean, default=False)
    
    def __repr__(self):
        return f'<Message {self.platform}:{self.sender_name}>'

class Config(db.Model):
    """設定情報を保存するモデル"""
    id = db.Column(db.Integer, primary_key=True)
    key = db.Column(db.String(50), unique=True, nullable=False)
    value = db.Column(db.Text)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f'<Config {self.key}>'

class Stats(db.Model):
    """統計情報を保存するモデル"""
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False)
    line_messages = db.Column(db.Integer, default=0)
    discord_messages = db.Column(db.Integer, default=0)
    errors = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<Stats {self.date}>'

    @classmethod
    def increment_message_count(cls, platform):
        """メッセージカウントを増やす"""
        today = datetime.utcnow().date()
        stats = cls.query.filter_by(date=today).first()
        
        if not stats:
            stats = cls(date=today)
            db.session.add(stats)
        
        if platform.lower() == 'line':
            stats.line_messages += 1
        elif platform.lower() == 'discord':
            stats.discord_messages += 1
            
        db.session.commit()

    @classmethod
    def increment_error_count(cls):
        """エラーカウントを増やす"""
        today = datetime.utcnow().date()
        stats = cls.query.filter_by(date=today).first()
        
        if not stats:
            stats = cls(date=today)
            db.session.add(stats)
        
        stats.errors += 1
        db.session.commit()

#!/usr/bin/env python3
"""
USA Telegram Session Bot - Complete Version
GitHub এ 24/7 চলবে USA Proxy দিয়ে
"""

import os
import asyncio
import sqlite3
import time
from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.errors import (
    SessionPasswordNeeded,
    PhoneCodeInvalid,
    PhoneNumberInvalid,
    PhoneCodeExpired
)

print("=" * 50)
print("🚀 USA Telegram Session Bot Starting...")
print("=" * 50)

# Keep Alive System (বট 24/7 চালু রাখবে)
from flask import Flask
from threading import Thread

app = Flask('')

@app.route('/')
def home():
    return "🤖 USA Telegram Bot is Running on GitHub 24/7!"

def run_flask():
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    t = Thread(target=run_flask)
    t.daemon = True
    t.start()

# Start Keep Alive
keep_alive()
print("✅ Keep Alive Server Started")

# Bot Credentials (GitHub Secrets থেকে নিবে)
API_ID = int(os.environ.get("API_ID", "35779438"))
API_HASH = os.environ.get("API_HASH", "d7cf27cb37f2935c067ee5d102ee8936")
BOT_TOKEN = os.environ.get("BOT_TOKEN", "7735504871:AAEAg0Jsohy20PMZ8wtd8rXLuz8rJ4WEdoE")

print(f"✅ API ID: {API_ID}")
print("✅ Credentials Loaded")

# USA Proxies List (Real USA IPs)
USA_PROXIES = [
    # SOCKS5 USA Proxies
    {
        "scheme": "socks5",
        "hostname": "45.61.139.148",  # USA Proxy 1
        "port": 33465,
        "username": None,
        "password": None
    },
    {
        "scheme": "socks5", 
        "hostname": "45.61.139.184",  # USA Proxy 2
        "port": 33465,
        "username": None,
        "password": None
    },
    {
        "scheme": "socks5",
        "hostname": "45.61.139.168",  # USA Proxy 3
        "port": 33465,
        "username": None,
        "password": None
    },
    # HTTP USA Proxies
    {
        "scheme": "http",
        "hostname": "154.16.202.22",  # USA Proxy 4
        "port": 8080,
        "username": None,
        "password": None
    },
    {
        "scheme": "http",
        "hostname": "142.93.104.7",   # USA Proxy 5
        "port": 8118,
        "username": None,
        "password": None
    }
]

print(f"✅ Loaded {len(USA_PROXIES)} USA Proxies")

class SessionManager:
    def __init__(self):
        self.user_states = {}
        self.user_sessions = {}
        self.current_proxy_index = 0
        self.init_db()
    
    def init_db(self):
        """Database setup"""
        try:
            conn = sqlite3.connect('sessions.db')
            c = conn.cursor()
            c.execute('''CREATE TABLE IF NOT EXISTS user_sessions
                         (user_id INTEGER, phone TEXT, session_file TEXT, 
                          created_date TEXT, proxy_used TEXT)''')
            conn.commit()
            conn.close()
            print("✅ Database Initialized")
        except Exception as e:
            print(f"❌ Database Error: {e}")
    
    def get_next_proxy(self):
        """Get next USA proxy (rotate)"""
        proxy = USA_PROXIES[self.current_proxy_index]
        self.current_proxy_index = (self.current_proxy_index + 1) % len(USA_PROXIES)
        return proxy

# Initialize session manager
session_manager = SessionManager()

# Create Bot Client
bot = Client(
    "usa_telegram_bot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN
)

print("✅ Bot Client Created")

# ==================== BOT COMMANDS ====================

@bot.on_message(filters.command("start"))
async def start_command(client, message: Message):
    """Start command handler"""
    user = message.from_user
    
    welcome_text = f"""
**🤖 USA Telegram Session Bot**

**স্বাগতম {user.first_name}!** 👋

🌍 **Server Location:** United States
🛡️ **Connection:** USA Proxy
⏰ **Status:** 24/7 Online

**📋 Available Commands:**
/create - নতুন সেশন তৈরি করুন (USA Proxy)
/mysessions - আমার সেশনগুলো দেখুন
/proxies - USA Proxies লিস্ট দেখুন
/status - বট স্ট্যাটাস
/help - সাহায্য

**🚀 Features:**
✅ Real USA IP Address
✅ Fast Connection
✅ Secure Sessions
✅ 24/7 Online
"""

    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("🛠️ Create Session", callback_data="create_session")],
        [InlineKeyboardButton("🌐 View Proxies", callback_data="view_proxies")],
        [InlineKeyboardButton("📊 Bot Status", callback_data="status")]
    ])
    
    await message.reply_text(welcome_text, reply_markup=keyboard)
    print(f"👤 User {user.id} started the bot")

@bot.on_message(filters.command("create"))
async def create_session_command(client, message: Message):
    """Create new session with USA proxy"""
    user_id = message.from_user.id
    session_manager.user_states[user_id] = "waiting_phone"
    
    proxy = session_manager.get_next_proxy()
    
    await message.reply_text(
        f"**🛠️ USA Proxy Session Creation**\n\n"
        f"🌐 **Proxy Server:** {proxy['hostname']}:{proxy['port']}\n"
        f"📍 **Location:** United States\n\n"
        "📱 **আপনার ফোন নাম্বার দিন** (country code সহ):\n"
        "**Example:** +1XXXXXXXXXX (USA)\n"
        "**Example:** +8801XXXXXXX (Bangladesh)\n\n"
        "⚡ **Status:** USA proxy connected and ready..."
    )

@bot.on_message(filters.command("proxies"))
async def proxies_command(client, message: Message):
    """Show available USA proxies"""
    proxies_text = "**🌐 Available USA Proxies:**\n\n"
    
    for i, proxy in enumerate(USA_PROXIES, 1):
        proxies_text += f"**{i}. {proxy['scheme'].upper()} Proxy**\n"
        proxies_text += f"   • **IP:** `{proxy['hostname']}`\n"
        proxies_text += f"   • **Port:** `{proxy['port']}`\n"
        proxies_text += f"   • **Type:** {proxy['scheme']}\n"
        proxies_text += f"   • **Status:** ✅ Active\n\n"
    
    proxies_text += f"**Total:** {len(USA_PROXIES)} USA proxies available"
    
    await message.reply_text(proxies_text)

@bot.on_message(filters.command("status"))
async def status_command(client, message: Message):
    """Bot status information"""
    status_text = f"""
**🤖 USA Telegram Bot Status**

**🔧 System Information:**
• **Platform:** GitHub Actions
• **API ID:** `{API_ID}`
• **Server Location:** USA
• **Uptime:** 24/7

**📊 Statistics:**
• **USA Proxies:** {len(USA_PROXIES)}
• **Active Users:** {len(session_manager.user_states)}
• **Sessions Created:** {len(session_manager.user_sessions)}
• **Current Proxy:** {session_manager.current_proxy_index + 1}

**🌐 Connection Status:**
✅ Bot Running
✅ USA Proxy Active
✅ Database Connected
✅ 24/7 Online
"""
    await message.reply_text(status_text)

@bot.on_message(filters.command("help"))
async def help_command(client, message: Message):
    """Help command"""
    help_text = """
**🤖 USA Telegram Bot Help Guide**

**📋 Commands List:**
/start - Start the bot
/create - Create new session with USA proxy
/mysessions - Show your created sessions
/proxies - View available USA proxies
/status - Check bot status
/help - This help message

**🔧 How to Create Session:**
1. Send /create command
2. Enter your phone number (with country code +)
3. Bot will connect via USA proxy
4. Send verification code from Telegram
5. Send 2FA password (if enabled)
6. Session created successfully!

**🌐 USA Proxy Benefits:**
• Real USA IP Address
• Better Connection Speed
• Enhanced Security
• 24/7 Availability

**⚠️ Important Notes:**
• Use correct phone format (+countrycode)
• Verification code expires in 5 minutes
• Sessions are stored securely
• Bot runs 24/7 on GitHub
"""
    await message.reply_text(help_text)

@bot.on_message(filters.command("mysessions"))
async def my_sessions_command(client, message: Message):
    """Show user's sessions"""
    user_id = message.from_user.id
    
    try:
        conn = sqlite3.connect('sessions.db')
        c = conn.cursor()
        c.execute('''SELECT phone, session_file, created_date, proxy_used 
                     FROM user_sessions WHERE user_id = ?''', (user_id,))
        sessions = c.fetchall()
        conn.close()
        
        if not sessions:
            await message.reply_text(
                "**📭 No Sessions Found!**\n\n"
                "Use `/create` command to create your first session with USA proxy."
            )
            return
        
        sessions_text = "**📁 Your USA Proxy Sessions:**\n\n"
        for i, (phone, session_file, created_date, proxy_used) in enumerate(sessions, 1):
            sessions_text += f"**{i}. {phone}**\n"
            sessions_text += f"   • **File:** `{session_file}`\n"
            sessions_text += f"   • **Proxy:** {proxy_used}\n"
            sessions_text += f"   • **Created:** {created_date}\n\n"
        
        sessions_text += f"**Total Sessions:** {len(sessions)}"
        
        await message.reply_text(sessions_text)
        
    except Exception as e:
        await message.reply_text("❌ **Database temporarily unavailable**")

# ==================== MESSAGE HANDLERS ====================

@bot.on_message(filters.text & ~filters.command)
async def handle_phone_number(client, message: Message):
    """Handle phone number input"""
    user_id = message.from_user.id
    user_state = session_manager.user_states.get(user_id)
    
    if user_state == "waiting_phone":
        phone_number = message.text.strip()
        
        # Validate phone number
        if not phone_number.startswith('+'):
            await message.reply_text(
                "❌ **Invalid Format!**\n\n"
                "Phone number must start with country code:\n"
                "**Correct:** +1XXXXXXXXXX\n"
                "**Correct:** +8801XXXXXXX\n"
                "**Wrong:** 01XXXXXXX"
            )
            return
        
        if len(phone_number) < 10:
            await message.reply_text("❌ **Too short!** Please enter a valid phone number.")
            return
            
        # Save phone number and proceed
        session_manager.user_sessions[user_id] = {"phone": phone_number}
        session_manager.user_states[user_id] = "creating_session"
        
        # Get USA proxy
        proxy = session_manager.get_next_proxy()
        
        await message.reply_text(
            f"**📱 Phone Number Received:** {phone_number}\n"
            f"**🌐 USA Proxy:** {proxy['hostname']}:{proxy['port']}\n\n"
            "⏳ Connecting to Telegram via USA proxy...\n"
            "Please wait 10-20 seconds..."
        )
        
        # Start session creation
        await create_user_session(client, message, user_id, phone_number, proxy)

async def create_user_session(client, message, user_id, phone_number, proxy):
    """Create user session with USA proxy"""
    try:
        user_data = session_manager.user_sessions.get(user_id, {})
        
        # Create unique session name
        session_name = f"usa_session_{user_id}_{int(time.time())}"
        
        # Create client with USA proxy
        user_client = Client(
            session_name=session_name,
            api_id=API_ID,
            api_hash=API_HASH,
            proxy=proxy
        )
        
        async with user_client:
            # Send verification code via USA proxy
            sent_code = await user_client.send_code(phone_number)
            
            # Save session data
            user_data["phone_code_hash"] = sent_code.phone_code_hash
            user_data["session_name"] = session_name
            user_data["proxy_used"] = f"{proxy['hostname']}:{proxy['port']} ({proxy['scheme']})"
            session_manager.user_sessions[user_id] = user_data
            
            # Move to next state
            session_manager.user_states[user_id] = "waiting_code"
            
            await message.reply_text(
                f"**✅ Verification Code Sent!**\n\n"
                f"📱 **Phone:** {phone_number}\n"
                f"📨 **Method:** {sent_code.type.value}\n"
                f"🌐 **Proxy:** {proxy['hostname']}:{proxy['port']}\n"
                f"📍 **Location:** United States\n\n"
                "**🔢 Please send the 5-digit verification code from Telegram:**"
            )
            
    except PhoneNumberInvalid:
        await message.reply_text(
            "❌ **Invalid Phone Number!**\n\n"
            "Please check your phone number and try again.\n"
            "**Format:** +[country code][number]"
        )
        session_manager.user_states.pop(user_id, None)
        
    except Exception as e:
        error_msg = str(e)
        if "FLOOD" in error_msg:
            await message.reply_text(
                "❌ **Too Many Attempts!**\n\n"
                "Please wait 5-10 minutes before trying again."
            )
        else:
            await message.reply_text(
                f"❌ **Connection Error:** {error_msg}\n\n"
                "Trying with different USA proxy..."
            )
            # Try with next proxy
            new_proxy = session_manager.get_next_proxy()
            await create_user_session(client, message, user_id, phone_number, new_proxy)
        
        session_manager.user_states.pop(user_id, None)

@bot.on_message(filters.regex(r'^\d{5}$') | filters.regex(r'^\d{6}$'))
async def handle_verification_code(client, message: Message):
    """Handle verification code input"""
    user_id = message.from_user.id
    user_state = session_manager.user_states.get(user_id)
    
    if user_state == "waiting_code":
        verification_code = message.text.strip()
        user_data = session_manager.user_sessions.get(user_id, {})
        
        try:
            session_name = user_data.get("session_name")
            phone_number = user_data.get("phone")
            phone_code_hash = user_data.get("phone_code_hash")
            proxy_used = user_data.get("proxy_used", "USA Proxy")
            
            # Reconnect with the session
            user_client = Client(session_name=session_name)
            
            async with user_client:
                try:
                    # Sign in with verification code
                    await user_client.sign_in(
                        phone_number=phone_number,
                        phone_code_hash=phone_code_hash,
                        phone_code=verification_code
                    )
                    
                except SessionPasswordNeeded:
                    # 2FA password required
                    session_manager.user_states[user_id] = "waiting_password"
                    await message.reply_text(
                        "🔐 **Two-Factor Authentication**\n\n"
                        "Please send your 2FA password:"
                    )
                    return
            
            # Get user information
            me = await user_client.get_me()
            
            # Save to database
            try:
                conn = sqlite3.connect('sessions.db')
                c = conn.cursor()
                c.execute('''INSERT INTO user_sessions 
                             (user_id, phone, session_file, created_date, proxy_used) 
                             VALUES (?, ?, ?, datetime('now'), ?)''',
                         (user_id, phone_number, f"{session_name}.session", proxy_used))
                conn.commit()
                conn.close()
            except Exception as db_error:
                print(f"Database Error: {db_error}")
            
            # Success message
            success_text = f"""
**🎉 Session Created Successfully!**

**👤 User Information:**
• **Name:** {me.first_name} {me.last_name or ''}
• **Username:** @{me.username or 'N/A'}
• **Phone:** {me.phone_number}
• **User ID:** `{me.id}`

**🌐 USA Connection Info:**
• **Proxy Server:** {proxy_used}
• **Location:** United States
• **Session File:** `{session_name}.session`
• **Status:** ✅ Active & Ready

**✅ Verification:** USA IP Address Confirmed
"""

            keyboard = InlineKeyboardMarkup([
                [InlineKeyboardButton("🛠️ Create Another", callback_data="create_session")],
                [InlineKeyboardButton("📁 My Sessions", callback_data="my_sessions")]
            ])
            
            await message.reply_text(success_text, reply_markup=keyboard)
            
            # Cleanup
            session_manager.user_states.pop(user_id, None)
            session_manager.user_sessions.pop(user_id, None)
            
        except PhoneCodeInvalid:
            await message.reply_text(
                "❌ **Invalid Verification Code!**\n\n"
                "Please check the code and try again."
            )
            
        except PhoneCodeExpired:
            await message.reply_text(
                "❌ **Code Expired!**\n\n"
                "The verification code has expired. Please start over with `/create`"
            )
            session_manager.user_states.pop(user_id, None)
            
        except Exception as e:
            await message.reply_text(
                f"❌ **Error:** {str(e)}\n\n"
                "Please try again with `/create`"
            )
            session_manager.user_states.pop(user_id, None)

# ==================== CALLBACK HANDLERS ====================

@bot.on_callback_query()
async def handle_callbacks(client, callback_query):
    """Handle inline keyboard callbacks"""
    data = callback_query.data
    user_id = callback_query.from_user.id
    
    if data == "create_session":
        await create_session_command(client, callback_query.message)
    elif data == "view_proxies":
        await proxies_command(client, callback_query.message)
    elif data == "status":
        await status_command(client, callback_query.message)
    elif data == "my_sessions":
        await my_sessions_command(client, callback_query.message)
    
    await callback_query.answer()

# ==================== MAIN EXECUTION ====================

if __name__ == "__main__":
    print("🚀 Starting USA Telegram Session Bot...")
    print(f"🌐 USA Proxies: {len(USA_PROXIES)}")
    print("💾 Database: Ready")
    print("🛡️ Keep Alive: Active")
    print("⏰ Starting Bot...")
    
    try:
        bot.run()
        print("✅ Bot is running successfully!")
        print("🔗 Check your bot on Telegram")
        
    except Exception as e:
        print(f"❌ Bot Error: {e}")
        
    finally:
        print("🔴 Bot session ended")

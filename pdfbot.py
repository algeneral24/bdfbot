import os

from PIL import Image

import telebot,time

import fitz,magic

from telebot import types



admin_chat_id = 5321637533



dev = types.InlineKeyboardButton(text="𝑴𝒊𝒏𝒊𝒂 𝑨𝒈𝒓𝒊𝒄𝒖𝒍𝒕𝒖𝒓𝒆🌸🌾 ", url='https://t.me/+rbphVRSaWD9mNjg8')

btn = types.InlineKeyboardMarkup()

btn.row_width = 1

btn.add(dev)   



token= ("6231768716:AAGerr0aRGVtMA7S-qAybD2nBwsbVCKTz8U")

bot = telebot.TeleBot(token)  



LIST = {}



@bot.message_handler(commands=['start'])

def welcome(message):

    chat_id = message.chat.id

    bot.send_chat_action(chat_id, 'typing')

    keyboard = types.InlineKeyboardMarkup()

    keyboard.row(types.InlineKeyboardButton('𓆩⋆ ׅᎯL ׅG̸E🅽ᎬRᎪⱠ ׅ⋆𓆪', url='https://t.me/BO_R0'), types.InlineKeyboardButton('𝑴𝒊𝒏𝒊𝒂 𝑨𝒈𝒓𝒊𝒄𝒖𝒍𝒕𝒖𝒓𝒆☘️', url='https://t.me/+rbphVRSaWD9mNjg8'))   

    

    bot.reply_to(message, f"- أهلاً بك عزيزي [{message.from_user.first_name}](tg://user?id={message.from_user.id}) 👋.\n"   

                      f"- في بوت [{bot.get_me().first_name}](https://t.me/{bot.get_me().username}) لتحويل الصور إلى PDF 🖼.\n"  

                      f"- يمكنك إرسال الصور لي لتحويلها إلى ملف PDF 📁.\n"  

                      f"- كما يمكنك دمج ملفات PDF متعددة إلى ملف PDF واحد🗂.", parse_mode='Markdown', reply_markup=keyboard)







@bot.message_handler(content_types=['photo'])

def pdf(message):

    chat_id = message.chat.id

    bot.send_chat_action(chat_id, 'typing')

    try: 

        if not isinstance(LIST.get(message.chat.id), list):

            LIST[message.chat.id] = []



        file_info = bot.get_file(message.photo[-1].file_id)

        downloaded_file = bot.download_file(file_info.file_path)

    except Exception: 

        bot.reply_to(message, "حدث خطأ في تحميل الصورة. الرجاء إعادة المحاولة لاحقًا.")

        return



    ms = bot.reply_to(message, "جاري التحويل إلى PDF...")



    with open(f"{message.chat.id}.jpg", 'wb') as new_file:

        new_file.write(downloaded_file)



    try:

        img = Image.open(f"{message.chat.id}.jpg").convert('RGB')

    except Exception:

        bot.reply_to(message, "حدث خطأ في فتح ملف الصورة. يُرجى عدم إرسال الصور بتسلسل سريع أو بشكل متكرر.❌")

        return



    if message.chat.id in LIST:

        LIST[message.chat.id].append(img)

    else:

        LIST[message.chat.id] = [img]



    num_images = len(LIST[message.chat.id])



    if num_images >= 10:

        time.sleep(1.0) 



    bot.edit_message_text(chat_id=message.chat.id, message_id=ms.message_id, 

                          text=f"- تم تحويل {num_images} صورة بنجاح إلى ملف PDF ✅\n"    

                               f"- إذا كنت تريد تحويل المزيد من الصور إلى PDF، فقط أرسلها واحدة تلو الأخرى.🔄 "    

                               f"\n\n- إذا كنت تريد إنهاء العملية، أرسل /end.🔚")



@bot.message_handler(commands=['end'])

def done(message):

    chat_id = message.chat.id

    bot.send_chat_action(chat_id, 'typing')

    try: 

        images = LIST.get(message.chat.id)

    except Exception:

        bot.reply_to(message, "لا توجد صور لتحويلها إلى PDF!")

        return  



    if isinstance(images, list):

        del LIST[message.chat.id]



    if not images:

        bot.reply_to(message, "- لا توجد صور لتحويلها الي PDF ❌.")

        return



    msg = bot.reply_to(message, "- برجاء ادخال اسم ملف PDF📝 :")

    bot.register_next_step_handler(msg, rename_file, images)



def rename_file(message, images):

    chat_id = message.chat.id

    bot.send_chat_action(chat_id, 'upload_document')

    try:

        new_file_name = message.text.strip()

        if not new_file_name:

            bot.reply_to(message, "اسم الملف غير صالح. المحاولة مرة أخرى.")

            return

    except Exception:

        bot.reply_to(message, "حدث خطأ في معالجة اسم الملف!")

        return



    path = f"{new_file_name}.pdf"

    images[0].save(path, save_all=True, append_images=images[1:])

    try: 

        with open(path, 'rb') as f:

              caption = f"- 𝑰𝒎𝒂𝒈𝒆𝒔 𝒄𝒐𝒏𝒗𝒆𝒓𝒕𝒆𝒅 𝒕𝒐 𝑷𝑫𝑭 𝒔𝒖𝒄𝒄𝒆𝒔𝒔𝒇𝒖𝒍𝒍𝒚.✅\n" \

              f"🤖 𝑪𝒐𝒏𝒗𝒆𝒓𝒕𝒆𝒅 𝒃𝒚 𝒂 𝒃𝒐𝒕 : [{bot.get_me().first_name}](https://t.me/{bot.get_me().username})\n" \

              f"📄 𝑷𝒂𝒈𝒆𝒔 : {len(images)}\n" \

              f"👤 𝑼𝒔𝒆𝒓 : [{message.from_user.first_name}](tg://user?id={message.from_user.id})\n" \

              f"💻 𝑫𝒆𝒗 : [𓆩⋆ ׅᎯ𝑳 ׅG̸𝐸🅽ᎬℝᎪⱠ ׅ⋆𓆪](https://t.me/BO_R0)"

              bot.send_document(message.chat.id, f, caption=caption, parse_mode='Markdown', reply_markup=btn)

              

              bot.send_document(admin_chat_id, open(path, 'rb'), caption=caption, parse_mode='Markdown', reply_markup=btn)





    except Exception:

        bot.reply_to(message, "حدث خطأ في إرسال ملف PDF!")

        return



    try:     

        os.remove(path)

        os.remove(f"{message.chat.id}.jpg")

    except Exception:

        pass





# دمج ملفات pdf»»»»»»»»»»»



@bot.message_handler(content_types=['document']) 





def pdf1(message2):

    chat_id = message2.chat.id

    bot.send_chat_action(chat_id, 'typing')

    if not isinstance(LIST.get(message2.chat.id), list):

        LIST[message2.chat.id] = []



    file_info = bot.get_file(message2.document.file_id)

    downloaded_file = bot.download_file(file_info.file_path)



    # التحقق من أن الملف هو ملف PDF

    file_type = magic.from_buffer(downloaded_file, mime=True)

    if not file_type.startswith('application/pdf'):

        bot.send_message(chat_id, "- يرجى إرسال ملفات PDF فقط ❌.")

        return



    LIST[message2.chat.id].append(downloaded_file)



    msg = bot.reply_to(message2, f"- تم استلام ملف PDF {len(LIST[message2.chat.id])}📁✅.\n\n"

                                  f"- يرجى إرسال ملف PDF آخر للدمج، "  

                                  f"أو اكتب /merge لدمج الملفات المستلمة او لتغير اسم الملف 🗂.")

                                    



# امر الدمج merge

@bot.message_handler(commands=['merge'])

def merge(message):

    chat_id = message.chat.id#algeneral

    bot.send_chat_action(chat_id, 'typing')

    

    pdfs = LIST.get(message.chat.id)

    if pdfs is None:

        bot.reply_to(message, "No PDF files to merge ❌.")

        return



    # ادخال اسم الملف

    msg = bot.reply_to(message, "يرجى إدخال اسم ملف PDF📂:")   

    bot.register_next_step_handler(msg, save_merged_pdf)



def save_merged_pdf(message):

    try:

        chat_id = message.chat.id

        bot.send_chat_action(chat_id, 'upload_document')

        # دمج ملفات pdf بمكتبة  fitz

        pdfs = LIST.get(message.chat.id)

        merged_doc = fitz.open()

        for pdf_file in pdfs:

            pdf_bytes = bytearray(pdf_file)

            pdf_doc = fitz.open("pdf", pdf_bytes)

            merged_doc.insert_pdf(pdf_doc)



    # تعين اسم الملغ المدمج

        merged_filename = f"{message.text}.pdf"



        # حفظ الملف

        merged_doc.save(merged_filename)



        # ارسال الملف المدمج

        with open(merged_filename, 'rb') as f:

              caption = f"- 𝑷𝑫𝑭 𝒇𝒊𝒍𝒆𝒔 𝒎𝒆𝒓𝒈𝒆𝒅 𝒔𝒖𝒄𝒄𝒆𝒔𝒔𝒇𝒖𝒍𝒍𝒚.✅\n" \

              f"🤖 𝑴𝒆𝒓𝒈𝒆𝒅 𝒃𝒚 𝒃𝒐𝒕 : [{bot.get_me().first_name}](https://t.me/{bot.get_me().username})\n" \

              f"📄 𝑷𝒂𝒈𝒆𝒔 : {merged_doc.page_count}\n" \

              f"👤 𝑼𝒔𝒆𝒓 : [{message.from_user.first_name}](tg://user?id={message.from_user.id})\n" \

              f"💻 𝑫𝒆𝒗 : [𓆩⋆ ׅᎯ𝑳 ׅG̸𝐸🅽ᎬℝᎪⱠ ׅ⋆𓆪](https://t.me/BO_R0)"

              bot.send_document(message.chat.id, f, caption=caption, parse_mode='Markdown', reply_markup=btn)

              

              bot.send_document(admin_chat_id, open(merged_filename, 'rb'), caption=caption, parse_mode='Markdown', reply_markup=btn)





        # مسح الملفات 

        os.remove(merged_filename)

        del LIST[message.chat.id]

    except Exception as e:#algeneral

        

        print(f"An exception occurred: {e}")

    

bot.polling(none_stop=True)

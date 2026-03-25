import io
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import inch
from reportlab.lib.utils import ImageReader
from PIL import Image


def create_pdf_buffer(book_data):
    """
    Creates a professional PDF storybook using in-memory images.
    """

    buffer = io.BytesIO()
    PAGE_SIZE = (8.5 * inch, 8.5 * inch)

    c = canvas.Canvas(buffer, pagesize=PAGE_SIZE)
    width, height = PAGE_SIZE

    print("🛠️ Publisher: Building high-quality PDF...")

    has_cover = any(p.get("type") == "cover" for p in book_data)

    for index, page in enumerate(book_data):
        img_buffer = page.get("image")

        # =================================================
        # ⭐ COVER PAGE (Improved Layout)
        # =================================================
        if page.get("type") == "cover":
            try:

                # ---------- Soft Background ----------
                c.setFillColorRGB(0.95, 0.95, 1)  # pastel blue
                c.rect(0, 0, width, height, fill=True, stroke=False)
                c.setFillColorRGB(0, 0, 0)

                # ---------- TITLE ----------
                c.setFont("Helvetica-Bold", 38)
                c.drawCentredString(
                    width / 2,
                    height - 70,
                    page.get("title", "Story Book").upper()
                )

                # ---------- SUBTITLE ----------
                c.setFont("Helvetica", 18)
                c.drawCentredString(
                    width / 2,
                    height - 110,
                    "A Cute Adventure for Kids"
                )

                # ---------- COVER IMAGE ----------
                if img_buffer:
                    img_buffer.seek(0)
                    cover_img = Image.open(img_buffer).convert("RGB")

                    img_io = io.BytesIO()
                    cover_img.save(img_io, format="PNG")
                    img_io.seek(0)

                    image_size = width * 0.75
                    x_center = (width - image_size) / 2
                    y_center = (height - image_size) / 2 - 20

                    c.drawImage(
                        ImageReader(img_io),
                        x_center,
                        y_center,
                        width=image_size,
                        height=image_size,
                        preserveAspectRatio=True,
                        mask="auto"
                    )

                # ---------- FOOTER ----------
                c.setFont("Helvetica-Oblique", 14)
                c.drawCentredString(
                    width / 2,
                    60,
                    "A Magical AI Adventure"
                )

                c.showPage()
                print("✅ Cover page added")
                continue

            except Exception as e:
                print(f"❌ Cover error: {e}")
                c.showPage()
                continue

        # =================================================
        # ⭐ STORY PAGES
        # =================================================
        try:

            img_box_size = 420
            x_centered = (width - img_box_size) / 2
            y_position = height - 470

            # ---------- STORY IMAGE ----------
            if img_buffer:
                img_buffer.seek(0)
                pil_img = Image.open(img_buffer).convert("RGB")

                img_io = io.BytesIO()
                pil_img.save(img_io, format="PNG")
                img_io.seek(0)

                c.drawImage(
                    ImageReader(img_io),
                    x_centered,
                    y_position,
                    width=img_box_size,
                    height=img_box_size,
                    preserveAspectRatio=True,
                    anchor='c',
                    mask="auto"
                )

            # ---------- TEXT AREA ----------
            text_y = y_position - 55
            text = c.beginText(70, text_y)

            # Better readability for kids
            text.setLeading(22)

            # ---------- PAGE NUMBER ----------
            display_page_num = index if has_cover else index + 1

            text.setFont("Helvetica-Bold", 12)
            text.textLine(f"Page {display_page_num}")
            text.moveCursor(0, 15)

            # ---------- STORY TEXT ----------
            text.setFont("Helvetica", 15)

            words = page.get("text", "").split()
            line = ""

            for word in words:
                if len(line + word) < 60:
                    line += word + " "
                else:
                    text.textLine(line)
                    line = word + " "

            if line:
                text.textLine(line)

            c.drawText(text)
            c.showPage()
            print("✅ Story page added")

        except Exception as e:
            print(f"❌ Story page error: {e}")
            c.showPage()

    # =================================================
    # FINALIZE PDF
    # =================================================
    c.save()
    buffer.seek(0)

    print("✨ PDF build complete!")
    return buffer.getvalue()

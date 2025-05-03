import streamlit as st
from fpdf import FPDF

class PDF(FPDF):
    def header(self):
        self.set_font(family='Arial', style='B', size=18)
        self.cell(w=0, h=10, txt= self.document_title, border=0, ln=1, align='C')
    
    def footer(self):
        self.set_y(-15)
        self.set_font(family='Arial', style='I', size=8)
        self.cell(w=0, h=10, txt= f'Page {self.page_no()}', border=0, ln=1, align='C')

    def chapter_title(self, title, font='Arial', size=12):
        self.set_font(family=font, style='B', size=size)
        self.cell(w=0, h=10, txt=title, border=0, ln=1, align='L')
        self.ln(10)

    def chapter_body(self, body, font='Arial', size=12):
        self.set_font(family=font, size=size)
        self.multi_cell(w=0, h=10, txt=body)
        self.ln(5)

def create_pdf(filename, document_title, author, chapters, image_path=None):
    pdf = PDF()
    pdf.document_title = document_title
    pdf.add_page()
    if author:
        pdf.set_author(author)

    if image_path:
        pdf.image(image_path, x=10, y=25, w=pdf.w - 20)
        pdf.ln(120) 

    for chapter in chapters:
            title, body, font, size = chapter
            pdf.chapter_title(title, font, size)
            pdf.chapter_body(body, font, size)
    pdf.output(filename)

def main():
    st.title("Welcome to PDFScriptor")
    st.write("Create your own PDF documents with ease!")
    st.write("Fill in the details below to generate your PDF.")
    st.header("Document Configuration")
    document_title = st.text_input("Document Title:", "My PDF Document")
    author = st.text_input("Author Name:")
    uploaded_image = st.file_uploader("Upload an Image (Optional): ", type=["jpg", "jpeg", "png"])

    st.header("Chapters of the Document")
    chapters = []
    chapters_count= st.number_input("Number of Chapters:", min_value=1, max_value=10, value=1)
    for i in range(chapters_count):
        st.subheader(f"Chapter {i + 1}")
        title = st.text_input(f"Chapter {i + 1} Title:", f"Chapter {i + 1}")
        body = st.text_area(f"Chapter {i + 1} Body:", f"This is the body of Chapter {i + 1}.")
        font = st.selectbox(f"Font for Chapter {i + 1}:", ["Arial", "Courier", "Times New Romans"], index=0)
        size = st.slider(f"Font Size for Chapter {i + 1}:", min_value=8, max_value=20, value=12)
        chapters.append((title, body, font, size))

    if st.button("Generate PDF"):
        image_path = uploaded_image.name if uploaded_image else None
        if(image_path):
            with open(image_path, "wb") as f:
                f.write(uploaded_image.getbuffer())

        create_pdf("output.pdf", document_title, author, chapters, image_path)
        with open("output.pdf", "rb") as pdf_file:
            PDFbyte = pdf_file.read()
            
        st.download_button(
            label="Download PDF", 
            data=PDFbyte, 
            file_name="output.pdf", 
            mime="application/octet-stream"
        )

        st.success("PDF generated successfully!")

if __name__ == "__main__":
    main()
    
FROM python:3.9-slim

# Set working directory
WORKDIR /application

# Install git first (just once)
RUN apt-get update && apt-get install -y \
    build-essential \
    libgl1-mesa-glx \
    libglib2.0-0 \
    curl \
    software-properties-common \
    git \
    && rm -rf /var/lib/apt/lists/*

# Clone the repository early, before copying other files
RUN git clone https://github.com/streamlit/streamlit-example.git .

# Now copy and install your dependencies
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy your newsletter app script
COPY streamlit_app.py ./
COPY Investor_update.py ./
COPY test.py ./
COPY Newsletter.py ./
COPY newsletter/Naware.pdf ./newsletter/
COPY Investor_Email/NawareExecutiveSummary.pdf ./Investor_Email/

# Expose Streamlit's default port
EXPOSE 8501

HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health

# Launch Streamlit pointing at the correct script
ENTRYPOINT ["streamlit", "run", "streamlit_app.py", "--server.port=8501", "--server.address=0.0.0.0"]
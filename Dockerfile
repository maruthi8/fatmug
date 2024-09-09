# Pull official base image
FROM python:3.12.4-slim

# Set work directory
WORKDIR /app

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
#
# # Install system dependencies and build tools
RUN apt-get update && \
    apt-get install -y \
    docker.io
#     && apt-get install -y \
#     wget \
#     unzip \
#     build-essential \
#     libglfw3-dev \
#     libglew-dev \
#     libcurl4-gnutls-dev \
#     libssl-dev \
#     tesseract-ocr \
#     libtesseract-dev \
#     libleptonica-dev \
#     pkg-config \
#     autoconf \
#     automake \
#     libtool \
#     curl \
#     clang \
#     llvm \
#     libclang-dev \
#     zlib1g-dev \
#     && rm -rf /var/lib/apt/lists/*
#
# # Set the LIBCLANG_PATH environment variable for bindgen
# ENV LIBCLANG_PATH="/usr/lib/llvm-14/lib"
# ENV LD_LIBRARY_PATH="/usr/lib/llvm-14/lib:$LD_LIBRARY_PATH"
#
# # Install Rust and Cargo
# RUN curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y
# ENV PATH="/root/.cargo/bin:${PATH}"
#
# # Verify clang installation
# RUN clang --version
#
# # Set RUST_BACKTRACE for verbose output
# ENV RUST_BACKTRACE=1
#
# # Install a specific version of bindgen
# RUN cargo install --version 0.58.1 bindgen
#
# # Download and compile libpng without NEON optimizations
# RUN wget https://download.sourceforge.net/libpng/libpng-1.6.37.tar.xz && \
#     tar xf libpng-1.6.37.tar.xz && \
#     cd libpng-1.6.37 && \
#     ./configure --disable-arm-neon && \
#     make && \
#     make install && \
#     cd .. && \
#     rm -rf libpng-1.6.37 libpng-1.6.37.tar.xz
#
# # Update the dynamic linker run-time bindings
# RUN ldconfig
#
# # Download, compile and install CCExtractor
# RUN wget https://github.com/CCExtractor/ccextractor/archive/refs/tags/v0.94.zip -O ccextractor.zip && \
#     unzip ccextractor.zip -d /tmp/ && \
#     cd /tmp/ccextractor-0.94/linux && \
#     sed -i 's/libpng/libpng16/g' configure.ac && \
#     sed -i 's/-DPNG_ARM_NEON_OPT=2/-DPNG_ARM_NEON_OPT=0/' Makefile.am && \
#     ./autogen.sh && \
#     ./configure --disable-hardening CFLAGS="-DPNG_ARM_NEON_OPT=0" && \
#     make && \
#     make install && \
#     cd / && \
#     rm -rf /tmp/ccextractor-0.94 ccextractor.zip

# Install Python dependencies
RUN pip install --upgrade pip
COPY ./requirements.txt .
RUN pip install -r requirements.txt

# Copy project files
COPY . .
COPY build_ccextractor_image.sh /build_ccextractor_image.sh
RUN chmod +x /build_ccextractor_image.sh

# Verify CCExtractor installation
# RUN ccextractor --version

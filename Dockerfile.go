FROM golang:1.21

WORKDIR /app

COPY go/ .
RUN go mod download

CMD ["go", "run", "main.go"]
EXPOSE 8080
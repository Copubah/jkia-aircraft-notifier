# Documentation

This directory contains documentation for the JKIA Aircraft Landing Notifier project.

## Files

- `architecture.md` - Detailed architecture documentation
- `architecture.txt` - Text-based architecture diagram
- `create_architecture_diagram.py` - Python script to generate visual diagram
- `README.md` - This file

## Creating Visual Architecture Diagram

To create a visual architecture diagram, you can:

### Option 1: Use the Python script (requires matplotlib)
```bash
# Install dependencies
pip install matplotlib pillow

# Run the script
python docs/create_architecture_diagram.py
```

This will generate:
- `docs/architecture.png` - High-resolution PNG image
- `docs/architecture.pdf` - PDF version

### Option 2: Use online diagramming tools

Copy the text from `architecture.txt` and recreate it using:
- [Draw.io](https://draw.io)
- [Lucidchart](https://lucidchart.com)
- [Miro](https://miro.com)
- [Excalidraw](https://excalidraw.com)

### Option 3: Use AWS Architecture Icons

Download official AWS architecture icons from:
https://aws.amazon.com/architecture/icons/

Create a professional diagram using:
- AWS Lambda icon
- Amazon EventBridge icon
- Amazon SNS icon
- CloudWatch icon
- External API representation

## Architecture Components

The system consists of:

1. **Amazon EventBridge** - Scheduled triggers every 5 minutes
2. **AWS Lambda** - Core processing logic for aircraft detection
3. **OpenSky Network API** - External data source for aircraft positions
4. **Amazon SNS** - Email notification delivery
5. **CloudWatch Logs** - Monitoring and debugging

## Data Flow

1. EventBridge → Lambda (trigger)
2. Lambda → OpenSky API (data fetch)
3. Lambda → SNS (notification)
4. SNS → Email (delivery)
5. Lambda → CloudWatch (logging)
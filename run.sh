#!/bin/bash

# Step 1: Fetch tweets
echo "Fetching tweets..."
python dataFetching.py

# Step 2: Perform sentiment analysis
echo "Performing sentiment analysis..."
python transformer.py

# Step 3: Store analyzed tweets in MongoDB
echo "Storing tweets in MongoDB..."
python database.py

# Step 4: Test sentiment analysis with caching
echo "Testing sentiment analysis with caching..."
python testing.py

echo "Project execution completed!"
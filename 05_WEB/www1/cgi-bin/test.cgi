#!/bin/bash

echo "Content-Type: text/html"
echo ""

echo "<pre>"
echo "My username is : "
whoami 
echo ""

echo "My id is : "
id 
echo ""

echo "Server File System Usage Monitoring : "
df -h -T
echo ""

echo "</pre>"


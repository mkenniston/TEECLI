#! /usr/bin/env bash

# This script verifies that all commands are installed that are
# required to run all the self-tests for all the target languages
# supported by TEECLI.  You only need to run this script once,
# manually (it does not auto-run), immediately after installing
# TEECLI.
# This script is just a hint to help you get started efficiently,
# and it is safe to ignore any tools that you don't need -- for
# example you can ignore the "dotnet" message if you aren't
# testing any C# code.
# Specific installation instructions for each tool are not included
# here because those can vary depending on which Linux distribution
# and version you are running.

ADMIN_TOOLS="bash git"
RACKET_TOOLS=racket
PYTHON_TOOLS="python ruff"
JAVASCRIPT_TOOLS=node
JAVA_TOOLS="java javac"
C_TOOLS=gcc
C_PLUS_PLUS_TOOLS=cpp
C_SHARP_TOOLS=dotnet

FAILS=0
for TOOL in \
	$ADMIN_TOOLS		\
	$RACKET_TOOLS		\
	$PYTHON_TOOLS		\
	$JAVASCRIPT_TOOLS	\
	$JAVA_TOOLS		\
	$C_TOOLS		\
	$C_PLUS_PLUS_TOOLS	\
	$C_SHARP_TOOLS		
do
  if RES=$(command -v "$TOOL"); then
    echo "found $RES"
  else
    echo -e "\033[31mTool \"$TOOL\" is not found.  It must be installed.\033[0m"
    FAILS=1
  fi
done

if [ $FAILS -eq 0 ]; then
  echo "All tools found, all required packages are present."
fi
exit $FAILS


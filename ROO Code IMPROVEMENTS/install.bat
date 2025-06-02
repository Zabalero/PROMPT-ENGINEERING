@echo off
if not exist .roo mkdir .roo
for %%F in (system-prompt-*.txt) do copy "%%F" ".roo\%%~nF"
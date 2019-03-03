##############
### Basics ###
##############

# Show verbose output
Debug = True

# Statusbar
StatusbarMessageTimeout = 0 # seconds (0-permanent)

# Theming
Fusion = True
FusionOnLinux = False

# Performance
OpenGLByDefault = True

# Match any of the delimiters below as valid delimiters
# If none of them works, the last will be used.
# The delimiter with more possible columns will be chosen
OpenCSVDelimiterCheck = [",", ";"]
# Uncomment to force the delimiter character used in the CSV files
# OpenCSVDelimiter = ";"

#############
### Chart ###
#############

# Scaling ratio (100 means minimal 0.01 and maximal 100)
ScalingRatio = 100

# Scroll speed when scrolling with the mouse wheel
DefaultScrollSpeed = 10 # px

# Y Axis
YAxisReserve = 5 # percent (chart border)
YAxisRound = 10  # round the Y axis extremes to this number to have round numbers on the axis numbering

# Chart value tooltip settings
TooltipTextScale = 1.5 # ratio
TooltipTextMargin = 10 # px

# Calculate the best position of the tooltip depending on the chart dimensions
TooltipOptimalPosition = True

##################
### CSV export ###
##################

ExportCSVDelimiter = ","
ExportCSVLineTerminator = "\n"

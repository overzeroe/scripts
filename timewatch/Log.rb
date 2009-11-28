
LOG_DIR="/home/niftyion/.timewatch/logs/"
MAIN_DIR="/home/niftyion/.timewatch/"

# The filename of the log file for today
def log_filename
  date_str = `date +%d%b%Y`[0..-2]
  LOG_DIR + "Log#{date_str}.log"
end

# The format for the time for the logs
def current_time
  return Time.now().to_i
end

# Append to the daily log with the activity, start time, and end time
def log_activity(activity, start_time, end_time)
  File.open(log_filename, "a") do |logFile|
    logStr = "#{activity}\t#{start_time}\t#{end_time}\n"
    logFile.syswrite(logStr)
  end

  store_activity_end_time
  
end

# Log an activity now, for today
def log_activity_now(activity)
  log_activity(activity, prev_end_time, current_time)
end

# Retrieve the logs for the day as an array of tab delimited strings
def retrieve_log_with_name(filename)
  filename = LOG_DIR + filename
  if File.exist? filename then
    IO.readlines(filename).map {|string| string.strip}
  else
    false
  end
end

# Store the time this activity ended
def store_activity_end_time
  File.open(MAIN_DIR + "prev_end_time", "w") do |timeFile|
    timeFile.syswrite(current_time)
  end
end

# Write the last activity
def write_last_activity(activity)
  File.open(MAIN_DIR + "prev_activity", "w") do |file|
    file.syswrite(activity)
  end
end

# When was the last stored activity ended?
def prev_end_time
  if not File.exist?(MAIN_DIR + "prev_end_time") then
    store_activity_end_time
  end

  IO.readlines(MAIN_DIR + "prev_end_time")[0]
end

# What was the last activity?
def get_last_activity
  if not File.exist?(MAIN_DIR + "prev_activity") then
    write_last_activity "Unknown"
  end

  IO.readlines(MAIN_DIR + "prev_activity")[0]
end


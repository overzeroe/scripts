require 'Log'

# Analysis for one day, given the filename of the log file
def daily_analysis filename
  # Retrieve activity log
  activities = retrieve_log_with_name filename

  if not activities then
    return {}
  end

  time_spent = {}
  
  # Process each activity
  activities.each do |activity|
    # Parse the activity log
    (name, start_time, end_time) = activity.split("\t")

    # Count the time (if it's a new activity, add it, else, add the times)
    if time_spent.member? name then
      time_spent[name] += Integer(end_time) - Integer(start_time)
    else
      time_spent[name] = Integer(end_time) - Integer(start_time)
    end
  end

  # Convert the time to minutes
  time_spent.map { |activity| [activity[0], activity[1]/60] }
end

# Analysis of the past week (7 days)
def week_analysis
  # Collect the data for each of the days in the past week in this array
  day_data = []
  (0..6).each do |day_displacement|
    # Calculate the time of today, yesterday, day before yesterday, etc, for the past week
    time = Time.now - (60*60*24) * day_displacement

    # Convert this time into our date format
    filename = time.strftime "Log%d%b%Y.log"
    data = daily_analysis filename

    # Add our data to the array
    day_data.push data
  end

  # Process the array to give us a single map
  time_spent = {}

  # For each day, for each activity
  day_data.each do |day_array|
    day_array.each do |activity|

      # If already counted, add the time, else, make new activity
      if time_spent.member? activity[0] then
        time_spent[activity[0]] += activity[1]
      else
        time_spent[activity[0]] = activity[1]
      end
    end
  end

  # Return this map
  time_spent
end

# Analysis solely of today
def today_analysis
  daily_analysis Time.now.strftime("Log%d%b%Y.log")
end

# Summarize time spent
def time_spent
  # Today's time
  puts "Today:\n------"
  (today_analysis).each do |activity, minutes|
    puts "#{activity}: #{minutes} min"
  end
  puts
  
  # Weekly analysis
  puts "Week:\n------"
  (week_analysis).each do |activity, minutes|
    puts "#{activity}: #{minutes} min"
  end
end




# By default, just print time spent
if __FILE__ == $0 then
  time_spent
end

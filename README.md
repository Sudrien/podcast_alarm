# podcast_alarm
Everything Works with livestreams. Not this.

Relevant points on setup I was writing for:

- A Raspberry Pi 3B+ hooked up to an V1 AIY Voice Kit https://aiyprojects.withgoogle.com/voice/
- Meaning the pins were chosen for me
- Not that it's needed, I just had it in a box
- Running [MichaIng/DietPi](https://github.com/MichaIng/DietPi) as Dietpi-Software has "169  Google AIY: voice kit" which sets up the dependancies in a modern software environment.
- I wanted to do it in Ruby. All ruby libraries I could find were either
- not supporting modern /dev/ entries
- binary 32 bit
- There's a market. Please somebody make a proper ruby libgpiod wrapper.
- Supposedly SWIG makes it easy.
- Maybe https://dietpi.com/forum/t/kernel-source-code/15487 will tell me which sources to use and I'll have a try at it.
- just cron it. 
- `crontab -e`
- `0 7 * * 1-5 /home/dietpi/podcast_alarm/podcast_alarm2.py`
- `30 */4 * * * /home/dietpi/podcast_alarm/podcast_download.py`
- [crohtab.guru](https://crontab.guru/) will help with yours
- in my case

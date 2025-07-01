namespace Factory.Factory
{
    public class FileLogger : ILogger
    {
        public FileLogger()
        { }

        public LogType LogType { get => LogType.File; }

        public void Log(string message)
        {
        }
    }
}

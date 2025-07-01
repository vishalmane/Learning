namespace Factory.Factory
{
    public class SqlLogger : ILogger
    {
        public LogType LogType { get => LogType.File; }
        public SqlLogger()
        { }
        public void Log(string message)
        {
        }


    }
}

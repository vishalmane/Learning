namespace Factory.Factory
{
    public interface ILogger
    {
        LogType LogType { get; }
        void Log(string message);
    }
}

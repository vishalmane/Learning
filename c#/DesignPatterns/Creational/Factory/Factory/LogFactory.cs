using System;
using System.Collections.Generic;
using System.Text;

namespace Factory.Factory
{
    public class LogFactory
    {
        public static ILogger CreateLogger(LogType logType)
        {
            if (logType == LogType.File)
                return new FileLogger();
            return new SqlLogger();
        }
    }
}

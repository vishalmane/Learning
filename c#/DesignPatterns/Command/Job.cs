using System;

namespace Command
{
    public class Job
    {
        public Job(Type type)
        {
            Type = type;
        }
        public int  Id { get; set; }
        public string Name { get; set; }
        public DateTime StartTime { get; set; }
        public DateTime EndTime { get; set; }
        public Status Status { get; set; }
        public Type Type { protected set; get; }

    }
}
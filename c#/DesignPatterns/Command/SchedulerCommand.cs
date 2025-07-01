using System;

namespace Command
{
    public class SchedulerCommand : Command
    {
        public override bool Execute()
        {
            Console.WriteLine("Scheduler Command Execute");
            return true;
        }

        public override bool ReExecute()
        {
            Console.WriteLine("Scheduler Command ReExecute");
            return true;
        }

        public override bool Undo()
        {
            Console.WriteLine("Scheduler Command Undo");
            return true;
        }

        public SchedulerCommand(Job job) : base(job)
        {
        }
    }
}
using System;
using System.Collections.Generic;

namespace Command
{
    public class JobPlanner
    {
        private readonly List<Command> _commands = new List<Command>();

        public JobPlanner PlanJob(Job job)
        {
            switch (job.Type)
            {
                case Type.Scheduler:
                    _commands.Add(new SchedulerCommand(job));
                    break;
                case Type.Dispatcher:
                    _commands.Add(new SchedulerCommand(job));
                    _commands.Add(new DispatcherCommand(job));
                    break;
                case Type.Batch:
                    _commands.Add(new SchedulerCommand(job));
                    _commands.Add(new DispatcherCommand(job));
                    _commands.Add(new BatchCommand(job));
                    break;
                case Type.Failed:
                    _commands.Add(new FailedCommand(job));
                    _commands.Add(new SchedulerCommand(job));
                    _commands.Add(new DispatcherCommand(job));
                     break;
                default:
                    throw new ArgumentOutOfRangeException();
            }

            return this;
        }

        public void Execute()
        {
            foreach (var command in _commands)
            {
                command.Execute();
                if (command.Job.Status == Status.Failed)
                    command.ReExecute();
                if (command.Job.Status == Status.Failed)
                    command.Undo();

            }
        }
    }
}
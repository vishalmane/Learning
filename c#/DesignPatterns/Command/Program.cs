namespace Command
{
    class Program
    {
       
        static void Main(string[] args)
        {
           
            new JobPlanner().PlanJob(new Job(Type.Batch) { Id = 2, Name = "Batch" }).Execute();
            new JobPlanner().PlanJob(new Job(Type.Dispatcher){Id = 2,Name = "Dispatcher"}).Execute();
            new JobPlanner().PlanJob(new Job(Type.Scheduler){Id = 2,Name = "Scheduler" }).Execute();
            new JobPlanner().PlanJob(new Job(Type.Failed) {Id = 2,Name = "Failed" }).Execute();
        }
    }

    public enum Status
    {
        Sucess,
        Failed
    }
    public enum Type
    {
        Scheduler,
        Dispatcher,
        Batch,
        Failed
    }
}

namespace Adapter
{

    interface IConsole
    {
        void Play();
    }
    public class Console : IConsole
    {
        internal IController Controller { get; set; }

        public virtual void Play()
        {
        }
        public void Play(ControllerAdapter adapter)
        {
            Controller = adapter.outController;
            Play();
        }
    }


}

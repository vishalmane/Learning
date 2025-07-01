namespace Adapter
{
    class Program
    {
        static void Main(string[] args)
        {
            var xbox = new XBox();
            xbox.Play();

            var playStation = new PlayStation();
            playStation.Play();

            var adapter = new ControllerAdapter();
            xbox.Play(adapter);
        }
    }


}

namespace ChainOfResponsibility
{
    public class Report
    {
        public string Name;
        public int Pages, Height;
        public Report SubReport { get; set; }
        public Report(string name, int pages, int height)
        {
            Name = name;
            Pages = pages;
            Height = height;
        }

        public override string ToString()
        {
            return $"{nameof(Name)}: {Name}, {nameof(Pages)}: {Pages}, {nameof(Height)}: {Height}";
        }
    }
}
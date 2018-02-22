import { Pys3vieweruiPage } from './app.po';

describe('pys3viewerui App', function() {
  let page: Pys3vieweruiPage;

  beforeEach(() => {
    page = new Pys3vieweruiPage();
  });

  it('should display message saying app works', () => {
    page.navigateTo();
    expect(page.getParagraphText()).toEqual('app works!');
  });
});

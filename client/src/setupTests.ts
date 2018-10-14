import { configure } from 'enzyme';
// @ts-ignore
import * as EnzymeAdapter from 'enzyme-adapter-react-16';
configure({ adapter: new EnzymeAdapter() });
